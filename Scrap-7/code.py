import requests
import faker
import json
import csv

csvfile = open('details.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile)
csvwriter.writerow([
                   'Title', 'Location', 'Country', 'Experience', 'Sequence',
                   'Code', 'JobID', 'Apply Link'
                   ])

ua = faker.Faker().firefox()
head = {'Accept': 'application/json', 'User-Agent': ua}
site = 'https://mphasis.ripplehire.com/candidate/candidatejobsearch'

payload = {
    "page": 0,
    "search": "*:*",
    "token": "ty4DfyWddnOrtpclQeia",
    "source": "CAREERSITE",
    "pagesize": 5,
    "geo": "IND"
}
query = {
    "careerSiteUrlParams": json.dumps(payload),
    "lang": "en"
}

res = requests.post(url=site, headers=head, data=query)
details = json.loads(res.text)

with open('2.json', 'w') as file:
    file.write(res.text)

for i in details['jobVoList']:
    l = [
        i['jobTitle'], i['locations'], i['jobLocation'], i['jobReqExp'],
        i['jobSeq'], i['jobCode'], i['jobId'],
        'https://mphasis.ripplehire.com/candidate/?token=ty4DfyWddnOrtpclQeia&source=CAREERSITE#detail/job/'+i['jobId']
        ]

    csvwriter.writerow(l)
    l.clear()

csvfile.close()
