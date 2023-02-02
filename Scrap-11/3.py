"""Importing all the required libraries."""

import os
import re
import requests
import logging
import threading
import time

from datetime import date
from unidecode import unidecode
from job_meta_upload_script_v2 import JobsMeta
from config_v2 import DEV_MAIL, AUTHOR_NO


# Walmart Global Tech India
class Company_Name:
    '''Creating Walmart class containing all the methods.'''
    def __init__(self, company):
        filename = f'{company}_logs_{date.today().strftime("%d_%m_%Y")}.log'

        logging.basicConfig(filename=filename,
                            format='%(asctime)s - %(lineno)s - %(levelname)s - %(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p',
                            level=logging.INFO)
        self.company = company
        self.logger_obj = logging.getLogger()
        self.thread_lock = threading.Lock()

        self.job_meta_obj = JobsMeta(self.company, self.logger_obj)

        session = requests.Session()
        base_url = 'https://one.Walmart.com/bin/careers/onprem/elsearch.json'
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.6.20) Gecko/2017-04-09 14:36:31 Firefox/11.0'
            }
        query = {
            'min_exp': 0,
            'max_exp': 10,
            'data_source': 'in',
            'country': 'india',
            'keyword': None,
            'page': 1,
            'results_per_Page': 500,
            'sort_by': 'SCORE',
            'gtsCareer': True
            }

        try:
            response = session.get(base_url, headers=header, params=query)
            self.json_data = response.json()

        except Exception as resp_err:
            self.logger_obj.critical(f'Error while requesting and getting json data from {self.base_url} : {resp_err}')
            self.job_meta_obj.exit_fun()

        self.count = int(self.json_data['numFound'])
        print('Total jobs found', self.count)

    def link_page(self, page=None):
        page_url = 'https://one.Walmart.com/content/globaltechindia/en_in/results.html?career_area=all&country=india'

        c = 0
        for job in self.json_data['results']:
            apply_link_ = job['apply_link']
            print(66, c)

            self.thread_lock.acquire()
            self.job_meta_obj.link_insertion(page_url, apply_link_)
            self.thread_lock.release()
            c += 1

    def new_scraper(self, page_job_urls):
        try:
            # page_url = page_job_urls[0]
            # job_url = page_job_urls[1]

            ex_stat = 'Not Existing'
            c = 0
            for job in self.json_data['results']:
                title_ = job['title']
                job_code_ = job['job_code']
                try:
                    job_func_ = job['job_function']
                except:
                    job_func_= None
                quali_ = job['preferred_qualifications_en']
                min_quali_ = job['min_qualifications_en']
                min_exp_ = job['min_experience']
                max_exp_ = job['max_experience']
                city_ = job['city']
                state_ = job['state']
                country_ = job['country']
                apply_link_ = job['apply_link']

                self.job_meta_obj.upload_job_meta_upload(postauth=AUTHOR_NO,
                    postcontent='', posttitle=title_, companyname='Walmart',
                    location=f'{city_} {state_} {country_}', jobtype='Permanent',
                    job_url=apply_link_, qualification=quali_,
                    skills=min_quali_, experience=min_exp_, salary=None,
                    imp_info=f'Job Category: {job_func_}',
                    company_website='https://one.Walmart.com/content/globaltechindia/en_in/careers.html',
                    company_tagline='Save Money, Live Better',
                    company_video='Not Available', company_twitter='@Walmart',
                    job_logo=True, localFilePath='./logo/Walmart.png')

                print(f'{c} {apply_link_} Scraped')

                self.job_meta_obj.change_status(apply_link_)

                c += 1

        except Exception as scr_err:
            self.logger_obj.error(f'Error in scraping for {apply_link_} : {scr_err}')


    def multi_thread_updated(self):
        '''multithreading.'''

        # pager=list(range(1,self.count+1))
        pager = 1
        
        '''Add Links to company_job_st_tb table with '''
        try:
            print(f'Total jobs on portal : {self.count}')

            self.link_page()

        except Exception as st_tb_mul_thd_err:
            self.logger_obj.critical(f'Error while inserting links in status table using multithreading : {st_tb_mul_thd_err}')
            print(f'Error while inserting links in status table using multithreading : {st_tb_mul_thd_err}')
            self.job_meta_obj.exit_fun()

        else:
            try:
                not_scraped_job_links = self.job_meta_obj.not_scraped_urls()
                print(f'Links remaining to be scraped : {len(not_scraped_job_links)}')

                # for i in not_scraped_job_links:
                #     threading.Thread(target=self.new_scraper, args=[i]).start()

                self.new_scraper(None)

                self.job_meta_obj.check_different('Walmart')
                print(f'Links remaining to be scraped : {len(self.job_meta_obj.not_scraped_urls())}')

            except Exception as job_scp_mt_err:
                self.logger_obj.critical(f'Error while inserting links in trial_job_meta using multithreading : {job_scp_mt_err}')
                self.job_meta_obj.exit_fun()

            else:
                self.job_meta_obj.delete_temp_table()

if __name__ == '__main__':
    start_time = time.time()

    obj = Company_Name('Walmart')
    obj.job_meta_obj.create_sc_stat_table()
    obj.multi_thread_updated()

    end_time = time.time()
    print('Time taken:', round(end_time-start_time, 2))

    if os.stat(f'{obj.company}_logs_{date.today().strftime("%d_%m_%Y")}.log').st_size!=0:
        obj.job_meta_obj.mail_log_file()
        print('Log file mailed')

    else:
        print('Log file is empty')
        logging.shutdown()
