'''Importing all the necessary libraries.'''

import hashlib
import os
import smtplib
import time
import requests
import mysql.connector
import config_v2

from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import date, datetime


class JobsMeta:
    '''
    Contains methods for performing database operations
    '''
    def __init__(self, company, logger_obj):
        '''
        Constructor for initial configuration for database connection
        '''
        self.logger_obj = logger_obj

        try:
            con_stat = internet_connection()  # Wait for 5/10 min

            if not con_stat[0]:
                self.logger_obj.critical(f'Internet Connectivity Issue : {con_stat[1]}')
                self.exit_fun()

            self.con = mysql.connector.connect(host=config_v2.DB_HOST,
                                               user=config_v2.DB_USER,
                                               password=config_v2.DB_PWD,
                                               database=config_v2.DB_NAME)
            self.cur = self.con.cursor(buffered=True)
            print('Connection Created')

        except Exception as con_err:
            self.logger_obj.critical(f'Error in connection to database {config_v2.DB_NAME} : {con_err}')
            self.exit_fun()

        else:
            self.company = company

    def create_sc_stat_table(self):
        '''
        Creating temporary table for job_url scraping status
        '''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            st_table = self.company.replace(' ', '_') + '_job_sc_stat'
            query = f"CREATE TABLE IF NOT EXISTS {st_table} (page_url VARCHAR(1000), job_url VARCHAR(1000), sc_stat VARCHAR(2)) ;"

            self.cur.execute(query)
            print(f'{self.company}_job_sc_stat Created')

        except Exception as crt_err:
            self.logger_obj.error(f'Error while creating table {self.company}_job_sc_stat : {crt_err}')

    def exit_fun(self):
        '''
        Stops the execution in case of critical error and sends the log file to respective developer
        '''
        self.mail_log_file()
        self.cur.close()
        self.con.close()

        raise Exception("Check log file")

    def db_reconnection(self):
        '''
        Reconnects to database
        Storing status instead of calling function in if condition as I need error part and for that
        again calling function would add sleep for 10min more
        '''
        try:
            con_stat = internet_connection()  # Wait for 5/10 min

            if not con_stat[0]:
                self.logger_obj.critical(f'Internet Connectivity Issue : {con_stat[1]}')
                self.exit_fun()

            self.con = mysql.connector.connect(host=config_v2.DB_HOST,
                                               user=config_v2.DB_USER,
                                               password=config_v2.DB_PWD,
                                               database=config_v2.DB_NAME)
            self.cur = self.con.cursor(buffered=True)

        except Exception as rec_err:
            self.logger_obj.critical(f'Error while reconnecting to {config_v2.DB_NAME} database : {rec_err}')
            return False

        return True

    def not_scraped_urls(self):
        '''
        Returns the list of Not Scraped(NS) job and page urls
        '''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            query = f"SELECT page_url,job_url FROM {self.company}_job_sc_stat WHERE sc_stat='NS'"
            self.cur.execute(query)
            not_scraped_records = self.cur.fetchall()

        except Exception as ns_err:
            self.logger_obj.critical(f'Error while selecting Not Scraped URLs from table {self.company}_job_sc_stat : {ns_err}')
            self.exit_fun()

        not_scraped_records = [list(i) for i in not_scraped_records]
        # print(120, not_scraped_records)
        return not_scraped_records

    def link_insertion(self, page_url, job_url):
        '''
        Inserts page and job url in the Scraping Status Table
        '''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            query = f"SELECT job_url FROM {self.company}_job_sc_stat WHERE job_url='{job_url}'"
            self.cur.execute(query)
            existing_job = self.cur.fetchall()

        except Exception as fth_err:
            self.logger_obj.error(f'''Error while checking if the job url {job_url} from page
                                    {page_url} already exists in status table {self.company}_job_sc_stat : {fth_err}''')

        else:
            if len(existing_job) == 0:  # Job_url does not exist in Scraping Status table
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()

                    query = f"INSERT INTO {self.company}_job_sc_stat VALUES('{page_url}','{job_url}','NS')"
                    self.cur.execute(query)
                    self.con.commit()
                    print(f'{self.company}_job_sc_stat inserted new link')

                except Exception as st_ins_err:
                    self.logger_obj.error(f'''Error while inserting the job url {job_url} from
                                                page {page_url} in status table {self.company}_job_sc_stat : {st_ins_err}''')

    def change_status(self, job_url):
        '''
        Changes the scraping status of the job url to S(Scraped)
        in Scraping Status Table
        '''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            query=f"UPDATE {self.company}_job_sc_stat SET sc_stat='S' WHERE job_url='{job_url}'"
            self.cur.execute(query)
            self.con.commit()

        except Exception as stat_chn_err:
            self.logger_obj.error(f'''Error while changing status for job url {job_url}
                                         in status table {self.company}_job_sc_stat : {stat_chn_err}''')

    def upload_job_meta_upload(self, postauth=16, postcontent='Work for Full Time',
                            posttitle='Developer', companyname='XYZ', location='India', jobtype='Full Time',
                            search_page_no='-1',job_url='https://www.xyz.in/apply-for-job/',
                            qualification='Graduation, Post Graduation', skills='Related to Job Title',
                            experience='0-2 years', salary='Not Disclosed',
                            imp_info='Candidate should be passionate about their work',
                            company_website='https://www.xyz.in/', company_tagline='Work Hard & Make History',
                            company_video='https://www.xyz.in/video/', company_twitter='@xyz', job_logo=False,
                            localFilePath='./logo/info.png'):
        '''
        Uploads the passed data in job data table
        '''
        try:
            md5_chksum = hashlib.md5((f"{postauth}, {postcontent}, {posttitle},\
{companyname},{location}, {jobtype}, {search_page_no},{job_url}, {qualification}, {skills},\
{experience},{salary}, {imp_info},{company_website}, {company_tagline},\
{company_video}, {company_twitter}, {job_logo},\
{localFilePath}").encode("utf-8")).hexdigest()

            if job_logo:
                job_logo = 1
            elif not job_logo:
                job_logo = 0

            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            query = f"SELECT md5_chksum FROM job_meta_2 WHERE md5_chksum='{md5_chksum}'"
            self.cur.execute(query)
            existing_job = self.cur.fetchall()

        except Exception as slc_err:
            self.logger_obj.error(f'Error while selecting md5 checksum from job_meta_2 table : {slc_err}')

        else:

            if len(existing_job) > 1:  # Deleting multiple copies of pre-existing jobs.
                if not self.con.is_connected():
                    if not self.db_reconnection():
                        self.exit_fun()

                try:
                    query = f"DELETE FROM job_meta_2 WHERE job_url='{job_url}'"
                    self.cur.execute(query)
                    self.con.commit()
                    print(f'{job_url} deleted due to duplication')

                except Exception as del_dup_err:
                    self.logger_obj.error(f'Error while deleting duplicate job {job_url} from job_meta_2 : {del_dup_err}')

                else:
                    try:
                        if not self.con.is_connected():
                            if not self.db_reconnection():
                                self.exit_fun()

                        time_stamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

                        query = f"""
                                INSERT INTO job_meta_2 (md5_chksum, postauth, postcontent, posttitle, companyname,
                                location, jobtype, search_page_no, job_url, qualification, skills, experience,
                                salary, imp_info, company_website, company_tagline, company_video,
                                company_twitter, job_logo, localFilePath, upld_date)
                                VALUES("{md5_chksum}",{postauth}, "{postcontent}", "{posttitle}",
                                "{companyname}", "{location}", "{jobtype}", "{search_page_no}","{job_url}",
                                "{qualification}", "{skills}", "{experience}", "{salary}",
                                "{imp_info}", "{company_website}", "{company_tagline}",
                                "{company_video}", "{company_twitter}", {job_logo}, 
                                "{localFilePath}", {time_stamp})
                            """
                        self.cur.execute(query)
                        self.con.commit()
                        print(f'{job_url} inserted updated one')

                    except Exception as job_ins_err:
                        self.logger_obj.error(f'Error while inserting job {job_url} in job_meta_2 : {job_ins_err}')

            elif len(existing_job) == 0:  # New md5 checksum so either we need to insert or update
                if not self.con.is_connected():
                    if not self.db_reconnection():
                        self.exit_fun()

                try:
                    '''
                    Checking whether the job url is already present or
                    not as md5 checksum is changed
                    '''
                    print(262)
                    query = f"SELECT job_url FROM job_meta_2 WHERE job_url='{job_url}'"
                    self.cur.execute(query)
                    existing_job = self.cur.fetchall()

                except Exception as sel_err:
                    self.logger_obj.error(f'Error while selecting apply url {job_url} : {sel_err}')

                else:
                    if len(existing_job) != 0:      # Job_url already exists so update the data
                        if not self.con.is_connected():
                            if not self.db_reconnection():
                                self.exit_fun()

                        try:
                            time_stamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

                            query = f"""
                                UPDATE job_meta_2 SET md5_chksum="{md5_chksum}",
                                postauth="{postauth}",postcontent="{postcontent}",posttitle="{posttitle}",
                                companyname="{companyname}",location="{location}",jobtype="{jobtype}",
                                search_page_no="{search_page_no}", qualification="{qualification}",skills="{skills}",
                                experience="{experience}",salary="{salary}",imp_info="{imp_info}",
                                company_website="{company_website}",company_tagline="{company_tagline}",
                                company_video="{company_video}",company_twitter="{company_twitter}",
                                job_logo="{job_logo}",localFilePath="{localFilePath},
                                upld_date="{time_stamp}"
                                WHERE job_url="{job_url}"
                            """
                            self.cur.execute(query)
                            self.con.commit()
                            print(f"{job_url} updated data")

                        except Exception as up_err:
                            self.logger_obj.error(f'Error while updating in job_meta_2 for job_url {job_url} : {up_err}')

                    else:   # Job_url is new so insert
                        if not self.con.is_connected():
                            if not self.db_reconnection():
                                self.exit_fun()

                        try:
                            time_stamp = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

                            query = f"""
                                        INSERT INTO job_meta_2 (md5_chksum, postauth, postcontent, posttitle,
                                        companyname, location, jobtype, search_page_no, job_url, qualification,
                                        skills, experience, salary, imp_info, company_website, company_tagline,
                                        company_video, company_twitter, job_logo, localFilePath, upld_date)
                                        VALUES("{md5_chksum}",{postauth}, "{postcontent}", "{posttitle}",
                                        "{companyname}", "{location}", "{jobtype}", "{search_page_no}","{job_url}",
                                        "{qualification}", "{skills}", "{experience}", "{salary}",
                                        "{imp_info}", "{company_website}", "{company_tagline}",
                                        "{company_video}", "{company_twitter}", {job_logo}, 
                                        "{localFilePath}", "{time_stamp}")
                                    """
                            self.cur.execute(query)
                            self.con.commit()
                            print(f'{job_url} inserted new')

                        except Exception as new_ins_err:
                            self.logger_obj.error(f'''Error while inserting in job_meta_2 for job_url {job_url} : {new_ins_err}''')

    def del_not_existing(self, job_url):
        '''
        Deletes the job url from Scraping status table that are
        not existing while scraping
        '''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            query = f"DELETE FROM {self.company}_job_sc_stat WHERE job_url='{job_url}'"
            self.cur.execute(query)
            self.con.commit()
            self.cur.close()
            self.con.close()

        except Exception as del_st_err:
            self.logger_obj.error(f'''Error while deleting not existing link from
                                         status table for {job_url} : {del_st_err}''')

    def check_different(self, companyname):
        '''
        Deleting jobs from job_meta_table that are also deleted
        from job site itself of same company.
        '''
        if not self.con.is_connected():
            if not self.db_reconnection():
                self.exit_fun()

        try:
            query = f"""
                        DELETE job_meta_2.*
                        FROM job_meta_2
                        LEFT OUTER JOIN {self.company}_job_sc_stat
                        ON job_meta_2.job_url = {self.company}_job_sc_stat.job_url
                        WHERE {self.company}_job_sc_stat.job_url IS NULL
                        AND job_meta_2.companyname = '{companyname}'
                    """
            self.cur.execute(query)
            self.con.commit()

        except Exception as del_err:
            self.logger_obj.error(f'Error while deleting jobs deleted from the site : {del_err}')

    def delete_temp_table(self):
        '''
        Drops the scraping status table once all job links
        have S as scraping status
        '''
        try:
            if not self.con.is_connected():
                if not self.db_reconnection():
                    self.exit_fun()

            query=f"SELECT page_url,job_url FROM {self.company}_job_sc_stat WHERE sc_stat='NS'"
            self.cur.execute(query)

        except Exception as ns_err:
            self.logger_obj.critical(f'''Error while selecting Not Scraped URLs
                                         from table {self.company}_job_sc_stat : {ns_err}''')
            self.exit_fun()

        else:
            not_scraped_links=[]

            if len(self.cur.fetchall()) == 0:
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()

                    query = f"DROP TABLE IF EXISTS {self.company}_job_sc_stat"
                    self.cur.execute(query)
                    self.con.commit()

                except Exception as del_st_table_err:
                    self.logger_obj.critical(f'''Error while deleting status table
                                                {self.company}_job_sc_stat : {del_st_table_err}''')
                    self.exit_fun()
            else:
                try:
                    if not self.con.is_connected():
                        if not self.db_reconnection():
                            self.exit_fun()

                    self.cur.execute(query)
                    not_scraped_links = self.cur.fetchall()
                    not_scraped_links = [list(i) for i in not_scraped_links]

                except Exception as fth_err:
                    self.logger_obj.critical(f'''Error while fetching Not Scraped URLs
                                                 from table {self.company}_job_sc_stat : {fth_err}''')
                    self.exit_fun()

        return not_scraped_links

    def mail_log_file(self):
        '''
        To mail the log file to respective developer
        Close all connections to database as
        mail will be sent only if execution is completed
        or in case of critical error
        '''
        self.cur.close()
        self.con.close()

        from_addr = config_v2.DEV_MAIL
        to_addr = 'sonymax@effobe.com'
        subject = f'Log File for {self.company} Job Portal'
        content = f'Please see the attached Log File for {self.company} Job Portal'

        con_stat = internet_connection()  # Wait for 2/10 min

        if not con_stat[0]:
            self.logger_obj.critical(f'Internet Connectivity Issue : {con_stat[1]}')
            self.exit_fun()

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        body = MIMEText(content, 'plain')
        msg.attach(body)

        filename = f'{self.company}_logs_{date.today().strftime("%d_%m_%Y")}.log'

        try:
            with open(filename, 'r', encoding="utf-8") as file:
                part = MIMEApplication(file.read(), Name=basename(filename))
                part['Content-Disposition'] = f'attachment; filename="{basename(filename)}"'

            msg.attach(part)
            file.close()

        except Exception as log_open_err:
            print(f'Error while reading log file {filename}: {log_open_err}')
            self.logger_obj.error(f'Error while reading log file {filename}: {log_open_err}')

        else:
            try:
                con_stat = internet_connection()  # Wait for 2/10 min

                if not con_stat[0]:
                    self.logger_obj.critical(f'Internet Connectivity Issue : {con_stat[1]}')
                    self.exit_fun()

                server = smtplib.SMTP('smtp.dreamhost.com', 587)
                server.login(from_addr, config_v2.DEV_PWD)
                server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])

            except Exception as em_log_err:
                print(f'Error while logging in to server and sending mail : {em_log_err}')
                self.logger_obj.error(f'Error while logging in and sending mail : {em_log_err}')

            server.quit()


def internet_connection():
    '''
    Check for internet connection and waits for
    minimum 2min and 10min max in case of connectivity issue
    '''
    trial = 0
    connect_error = ''
    url = "https://www.google.com"
    time_out = 10

    while trial != 5:  # Checks connection for maximum 5 times
        try:
            trial_req = requests.get(url, timeout=time_out)
            return [True, 0]

        except (requests.ConnectionError, requests.Timeout) as int_con_err:
            time.sleep(120)  # Sleep for 2min and check again
            trial += 1
            connect_error = int_con_err

    return [False, connect_error]
