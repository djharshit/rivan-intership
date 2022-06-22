import requests
import faker
import json
import csv

csvfile = open('details.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile)
csvwriter.writerow([
                   'Title', 'Location', 'Country', 'Date', 'JobID',
                   'Description', 'Requisition Type',
                   'Requisition Id', 'Job Schedule', 'Degree Level',
                   'Contract Type', 'Location Name', 'Apply Link'
                   ])

ua = faker.Faker().firefox()
head = {'User-Agent': ua}
site = 'https://fa-eumz-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions'
query = {
    'onlyData': True,
    'expand': 'all',
    'finder': 'findReqs;limit=200,sortBy=POSTING_DATES_DESC'
}

res = requests.get(url=site, headers=head, params=query)
data = json.loads(res.text)

for i in data['items'][0]['requisitionList']:
    job_id = i['Id']

    site = 'https://fa-eumz-saasfaprod1.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails'
    query = {
        'onlyData': True,
        'expand': 'all',
        'finder': f'ById;Id={job_id}'
    }
    res = requests.get(url=site, headers=head, params=query)
    data = json.loads(res.text).get('items')[0]
    # print(job_id, data['Title'])
    l = [
        data['Title'],
        data['PrimaryLocation'],
        data['PrimaryLocationCountry'],
        data['ExternalPostedStartDate'][:10],
        data['Id'],
        data['ShortDescriptionStr'],
        data['RequisitionType'],
        data['RequisitionId'],
        data['JobSchedule'],
        data['StudyLevel'],
        data['ContractType'],
    ]
    try:
        l.append(data['workLocation'][0]['LocationName'])
    except IndexError:
        l.append('Null')
    l.append(f'https://fa-eumz-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/job/{data["Id"]}/apply/email')

    csvwriter.writerow(l)
    l.clear()

csvfile.close()
