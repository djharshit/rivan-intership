'''Importing all the necessary libraries.'''

import mysql.connector as connector
import hashlib
import os
import smtplib
import config

from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class JobsMeta:
    def __init__(self, company, logger_obj, dev_mail):
        self.logger_obj = logger_obj
        self.dev_mail = config.DEV_MAIL
        self.company = company

        try:
            self.con = connector.connect(host=config.DB_HOST,
                                         user=config.DB_USER,
                                         password=config.DB_PWD,
                                         database=config.DB_NAME)
            self.c = self.con.cursor(buffered=True)
            print('Connection created')

        except Exception as con_err:
            self.logger_obj.critical(f'Error in connection to database {config.DB_NAME} : {con_err}')
            self.exit_fun(self.dev_mail)

    def create_sc_stat_table(self):
        '''Creating temporary table for job_url scraping status'''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun(self.dev_mail)

            st_table=self.company.replace(' ','_') + '_job_sc_stat'
            query = f"CREATE TABLE IF NOT EXISTS {st_table} (page_url VARCHAR(255), job_url VARCHAR(255), sc_stat VARCHAR(15)) ;"

            self.c.execute(query)
            print(f'{self.company}_job_sc_stat created')

        except Exception as crt_err:
            self.logger_obj.error(f'Error while creating table {self.company}_job_sc_stat : {crt_err}')
    
    def exit_fun(self,dev_mail):
        self.mail_log_file(dev_mail)
        exit()
    
    def db_reconnection(self):
        try:
            self.con = connector.connect(host=config.DB_HOST,
                            user=config.DB_USR,
                            password=config.DB_PWD,
                            database=config.DB_NAME)

            self.c = self.con.cursor(buffered=True)
        except Exception as rec_err:
            self.logger_obj.critical(f'Error while reconnecting to {DB_NAME} database : {rec_err}')
            return False
        else:
            return True

    def not_scraped_urls(self):
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun(self.dev_mail)

            query = f"SELECT page_url,job_url FROM {self.company}_job_sc_stat WHERE sc_stat='NS'"
            self.c.execute(query)
            not_scraped_records = self.c.fetchall()

        except Exception as ns_err:
            self.logger_obj.critical(f'Error while selecting Not Scraped URLs from table {self.company}_job_sc_stat : {ns_err}')
            self.exit_fun(self.dev_mail)

        else:
            not_scraped_records = [list(i) for i in not_scraped_records]
            # print(83, not_scraped_records)
            return not_scraped_records

    def link_insertion(self, page_url, job_url):
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun(self.dev_mail)

            query = f"SELECT job_url FROM {self.company}_job_sc_stat WHERE job_url='{job_url}'"
            self.c.execute(query)
            existing_job = self.c.fetchall()

        except Exception as fth_err:
            self.logger_obj.error(f'Error while checking if the job url {job_url} from page {page_url} already exists in status table {self.company}_job_sc_stat : {fth_err}')

        else:
            '''Checking if the url already exists'''
            if len(existing_job) == 0:
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun(self.dev_mail)

                    query=f"INSERT INTO {self.company}_job_sc_stat VALUES('{page_url}','{job_url}','NS')"
                    self.c.execute(query)
                    self.con.commit()
                    print(f'{self.company}_job_sc_stat inserted new link')

                except Exception as st_ins_err:
                    self.logger_obj.error(f'Error while inserting the job url {job_url} from page {page_url} in status table {self.company}_job_sc_stat : {st_ins_err}')

            else:
                print(existing_job, 'already exists')

    def change_status(self, job_url):
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun(self.dev_mail)

            query=f"UPDATE {self.company}_job_sc_stat SET sc_stat='S' WHERE job_url='{job_url}'"
            self.c.execute(query)
            self.con.commit()

        except Exception as stat_chn_err:
            self.logger_obj.error(f'Error while changing status for job url {job_url} in status table {self.company}_job_sc_stat : {stat_chn_err}')

    def upload_job_meta_upload(self, postauth, postcontent, posttitle, companyname,
                            location, jobtype, apply_url, qualification, skills,
                            experience, salary, imp_info, company_website,
                            company_tagline, company_video, company_twitter,
                            job_logo, localFilePath):
        try:
            md5_chksum = hashlib.md5((f"{postauth}, {postcontent}, {posttitle},\
{companyname},{location}, {jobtype}, {apply_url}, {qualification}, {skills},\
{experience},{salary}, {imp_info},{company_website}, {company_tagline},\
{company_video}, {company_twitter}, {job_logo},\
{localFilePath}").encode("utf-8")).hexdigest()

            if job_logo:
                job_logo = 1
            elif not job_logo:
                job_logo = 0

            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun(self.dev_mail)

            query = f"SELECT md5_chksum FROM trial_job_meta WHERE md5_chksum='{md5_chksum}'"
            self.c.execute(query)
            existing_job = self.c.fetchall()

        except Exception as slc_err:
            self.logger_obj.error(f'Error while selecting md5 checksum from trial_job_meta table : {slc_err}')

        else:
            '''Deleting multiple copies of pre-existing jobs.'''
            if len(existing_job) > 1:
                if not self.con.is_connected():
                    if not self.db_reconnection():
                        self.exit_fun(self.dev_mail)

                try:
                    query = f'DELETE FROM trial_job_meta WHERE apply_url="{apply_url}"'
                    self.c.execute(query)
                    self.con.commit()
                    print(f'{apply_url} deleted due to duplication')

                except Exception as del_dup_err:
                    self.logger_obj.error(f'Error while deleting duplicate job {apply_url} from trial_job_meta : {del_dup_err}')

                else:
                    try:
                        if not self.con.is_connected():
                            if not self.db_reconnection():
                                self.exit_fun(self.dev_mail)

                        query = f"""
                                INSERT INTO trial_job_meta(md5_chksum, postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath)
                                VALUES("{md5_chksum}",{postauth}, "{postcontent}", "{posttitle}",
                                "{companyname}", "{location}", "{jobtype}", "{apply_url}",
                                "{qualification}", "{skills}", "{experience}", "{salary}",
                                "{imp_info}", "{company_website}", "{company_tagline}",
                                "{company_video}", "{company_twitter}", {job_logo}, 
                                "{localFilePath}")
                            """
                        self.c.execute(query)
                        self.con.commit()
                        print(f'{apply_url} inserted updated one')

                    except Exception as job_ins_err:
                        self.logger_obj.error(f'Error while inserting job {apply_url} in trial_job_meta : {job_ins_err}')

            elif len(existing_job) == 0:
                '''Adding jobs that are new in job site to job_meta_data table.'''
                if not self.con.is_connected():
                    if not self.db_reconnection():
                        self.exit_fun(self.dev_mail)

                try:
                    '''Checking whether the url is already present or not as md5 checksum is changed'''
                    sel_qry=f"SELECT apply_url FROM trial_job_meta WHERE apply_url='{apply_url}'"
                    self.c.execute(sel_qry)
                    exist_job=self.c.fetchall()

                except Exception as sel_err:
                    self.logger_obj.error(f'Error while selecting apply url {apply_url} : {sel_err}')

                if len(exist_job)!=0:
                    '''Apply url already so we just need to update the data'''
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun(self.dev_mail)

                    try:
                        queryery=f"""
                            UPDATE trial_job_meta SET md5_chksum='{md5_chksum}',
                            postauth='{postauth}',postcontent='{postcontent}',posttitle='{posttitle}',
                            companyname='{companyname}',location='{location}',jobtype='{jobtype}',
                            qualification='{qualification}',skills='{skills}',
                            experience='{experience}',salary='{salary}',imp_info='{imp_info}',
                            company_website='{company_website}',company_tagline='{company_tagline}',
                            company_video='{company_video}',company_twitter='{company_twitter}',
                            job_logo='{job_logo}',localFilePath='{localFilePath}' WHERE apply_url='{apply_url}'
                        """
                        self.c.execute(queryery)
                        self.con.commit()
                        print(f"{apply_url} updated data")

                    except Exception as up_err:
                        self.logger_obj.error(f'Error while updating in trial_job_meta for apply_url {apply_url} : {up_err}')

                else:
                    '''Apply url does means we need to insert this new url data'''
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun(self.dev_mail)

                    try:
                        query = f"""
                                    INSERT INTO trial_job_meta(md5_chksum, postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath)
                                    VALUES("{md5_chksum}",{postauth}, "{postcontent}", "{posttitle}",
                                    "{companyname}", "{location}", "{jobtype}", "{apply_url}",
                                    "{qualification}", "{skills}", "{experience}", "{salary}",
                                    "{imp_info}", "{company_website}", "{company_tagline}",
                                    "{company_video}", "{company_twitter}", {job_logo}, 
                                    "{localFilePath}")
                                """
                        self.c.execute(query)
                        self.con.commit()
                        print(f'{apply_url} inserted new')
                        # rp_query=f"""
                        #             REPLACE INTO trial_job_meta(md5_chksum, postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath)
                        #             VALUES("{md5_chksum}",{postauth}, "{postcontent}", "{posttitle}",
                        #             "{companyname}", "{location}", "{jobtype}", "{apply_url}",
                        #             "{qualification}", "{skills}", "{experience}", "{salary}",
                        #             "{imp_info}", "{company_website}", "{company_tagline}",
                        #             "{company_video}", "{company_twitter}", {job_logo}, 
                        #             "{localFilePath}")
                        # """
                    except Exception as new_ins_err:
                        self.logger_obj.error(f'Error while inserting in trial_job_meta for apply_url {apply_url} : {new_ins_err}')

    def del_not_existing(self, job_url):
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun(self.dev_mail)

            query=f"DELETE FROM {self.company}_job_sc_stat WHERE job_url='{job_url}'"
            self.c.execute(query)
            self.con.commit()

        except Exception as del_st_err:
            self.logger_obj.error(f'Error while deleting not existing link from status table for {job_url} : {del_st_err}')

    def check_different(self, companyname):
        '''Deleting jobs from job_meta_table that are also deleted from job site itself of same company.'''
        if not self.con.is_connected():
            if not self.db_reconnection():
                self.exit_fun(self.dev_mail)

        try:
            query = f"""
                        DELETE trial_job_meta.*
                        FROM trial_job_meta
                        LEFT OUTER JOIN {self.company}_job_sc_stat
                        ON trial_job_meta.apply_url = {self.company}_job_sc_stat.job_url
                        WHERE {self.company}_job_sc_stat.job_url IS NULL
                        AND trial_job_meta.companyname = '{companyname}'
                    """

            self.c.execute(query)
            self.con.commit()

        except Exception as del_err:
            self.logger_obj.error(f'Error while deleting jobs deleted from the site : {del_err}')
    
    
    def delete_temp_table(self):
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun(self.dev_mail)

            query = f"SELECT page_url,job_url FROM {self.company}_job_sc_stat WHERE sc_stat='NS'"
            self.c.execute(query)

        except Exception as ns_err:
            self.logger_obj.critical(f'Error while selecting Not Scraped URLs from table {self.company}_job_sc_stat : {ns_err}')
            self.exit_fun(self.dev_mail)

        else:
            ns_link = []

            if len(self.c.fetchall()) == 0:
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun(self.dev_mail)

                    query = f"DROP TABLE IF EXISTS {self.company}_job_sc_stat"
                    self.c.execute(query)
                    self.con.commit()

                except Exception as del_st_tb_err:
                    self.logger_obj.critical(f'Error while deleting status table {self.company}_job_sc_stat : {del_st_tb_err}')
                    self.exit_fun(self.dev_mail)

            else:
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun(self.dev_mail)

                    self.c.execute(query)
                    ns_link = self.c.fetchall()
                    ns_link = [list(i) for i in ns_link]

                except Exception as fth_err:
                    self.logger_obj.critical(f'Error while fetching Not Scraped URLs from table {self.company}_job_sc_stat : {fth_err}')
                    self.exit_fun(self.dev_mail)

        return ns_link

    def mail_log_file(self, to_em_addr):
        from_addr = config.DEV_MAIL
        to_addr = to_em_addr
        subject = f'Log File for {self.company} Job Portal'
        content = f'Please see the attached Log File for {self.company} Job Portal'

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        body = MIMEText(content, 'plain')
        msg.attach(body)

        filename = f'{self.company}_logs.log'
        try:
            with open(filename, 'r') as f:
                part = MIMEApplication(f.read(), Name=basename(filename))
                part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
            msg.attach(part)

        except Exception as log_open_err:
            print(f'Error while reading log file {filename}: {log_open_err}')
            self.logger_obj.error(f'Error while reading log file {filename}: {log_open_err}')

        else:
            try:
                server = smtplib.SMTP('smtp.dreamhost.com', 587)
                server.login(from_addr, config.DEV_PWD)
                server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])

            except Exception as em_log_err:
                print(f'Error while logging in and sending mail : {em_log_err}')
                self.logger_obj.error(f'Error while logging in and sending mail : {em_log_err}')
