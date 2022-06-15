import requests
import json
import faker
import upload

jobs = upload.JobsMeta('ADP')

count = 1
fake = faker.Faker()

site = 'https://jobsapi-google.m-cloud.io/api/job/search'
head = {'User-Agent': fake.firefox()}
query = {
    'pageSize': 100,
    'offset': 0,
    'companyName': 'companies/c3f83ef5-c5b8-4d56-9c79-66f4052c4c4a',
    'languageCode[]': 'en',
    'customAttributeFilter': 'country="IN"',
    'orderBy': 'relevance desc'
}
res = requests.get(url=site, headers=head, params=query)

data = json.loads(res.text)

for i in data['searchResults']:
    jobs.upload_job_meta(postauth=16, postcontent='Work for Full Time', posttitle=i['job']['title'], companyname='ADP',
                        location=f"{i['job']['primary_state']} {i['job']['primary_country']}", jobtype='Full Time', apply_url=i['job']['seo_url'],
                        qualification='Graduation, Post Graduation', skills='Related to Job Title',
                        experience='0-2 years',
                        salary='Not Disclosed', imp_info='Candidate should be passionate about their work',
                        company_website='https://jobs.adp.com/', company_tagline='Not Available',
                        company_video='Not Available', company_twitter='@ADPCareers', job_logo=True,
                        localFilePath='./logo/adp.png')

    print(count)
    count += 1

jobs.check_different()
jobs.delete_temp_table()
jobs.con.close()
