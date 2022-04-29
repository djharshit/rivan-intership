import mysql.connector as connector


class JobsMeta:  # 1st
    def __init__(self, company):
        self.con = connector.connect(host='mysql.jobs.rivan.in',
                                     user='jobsrivanin',
                                     password='?t7up8Pi',
                                     database='jobs_rivan_in')

        self.c = self.con.cursor(buffered=True)
        print('Connection Created')

        self.company = company

        # Creating temporary table for updating job_meta_data.
        query = f"CREATE TABLE IF NOT EXISTS {company}_new_temp_table LIKE job_meta_data"
        self.c.execute(query)
        print(f'{self.company}_new_temp_table Created \n')

    def upload_job_meta(self, postauth=16, postcontent='Work for Full Time', posttitle='Developer', companyname='XYZ',
                        location='India', jobtype='Full Time', apply_url='https://www.xyz.in/apply-for-job/',
                        qualification='Graduation, Post Graduation', skills='Related to Job Title',
                        experience='0-2 years',
                        salary='Not Disclosed', imp_info='Candidate should be passionate about their work',
                        company_website='https://www.xyz.in/', company_tagline='Work Hard & Make History',
                        company_video='https://www.xyz.in/video/', company_twitter='@xyz', job_logo=False,
                        localFilePath='./logo/info.png'):

        if job_logo:
            job_logo = 1
        elif not job_logo:
            job_logo = 0

        # Insert all the records in the new temporary table.
        query = f"""
                    INSERT INTO {self.company}_new_temp_table(postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath)
                    VALUES(%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, "%s")
                """ % (
            postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills,
            experience,
            salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo,
            localFilePath)

        self.c.execute(query)
        self.con.commit()

        # checking of job_meta_data table.
        query = """
                    SELECT serial FROM job_meta_data WHERE apply_url="%s"
                """ % (
            apply_url
        )
        self.c.execute(query)
        existing_job = self.c.fetchall()

        # Deleting multiple copies of pre-existing jobs.
        if len(existing_job) > 1:
            query = """
                        DELETE FROM job_meta_data WHERE apply_url="%s"
                    """ % (
                apply_url
            )
            self.c.execute(query)
            self.con.commit()
            # print("Deleted duplicate records")

            query = """
                        INSERT INTO job_meta_data(postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath)
                        VALUES(%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, "%s")
                    """ % (
                postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills,
                experience,
                salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo,
                localFilePath)

            self.c.execute(query)
            self.con.commit()
            # print("Inserted single record")

        # Adding jobs that are new in job site to job_meta_data table.
        elif len(existing_job) == 0:
            query = """
                        INSERT INTO job_meta_data(postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills, experience, salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo, localFilePath)
                        VALUES(%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", %s, "%s")
                    """ % (
                postauth, postcontent, posttitle, companyname, location, jobtype, apply_url, qualification, skills,
                experience,
                salary, imp_info, company_website, company_tagline, company_video, company_twitter, job_logo,
                localFilePath)

            self.c.execute(query)
            self.con.commit()
            # print("Inserted new record")

    def check_different(self):

        # Deleting jobs from job_meta_table that are also deleted from job site itself.
        query = f"""
                    DELETE job_meta_data.*
                    FROM job_meta_data
                    LEFT OUTER JOIN {self.company}_new_temp_table
                    ON job_meta_data.apply_url = {self.company}_new_temp_table.apply_url
                    WHERE {self.company}_new_temp_table.apply_url IS NULL
                """

        self.c.execute(query)
        self.con.commit()

    def delete_temp_table(self):

        query = f"""
                    DROP TABLE IF EXISTS {self.company}_new_temp_table
                """

        self.c.execute(query)
        self.con.commit()
        # print(f'Deleted table {self.company}_new_temp_table')
