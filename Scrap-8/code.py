import requests
import faker
import json
import csv

csvfile = open('details.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile)
csvwriter.writerow([
                   'Title', 'Location', 'Country', 'Experience', 'Skills',
                   'Area', 'JobID', 'Requisition Id', 'Date', 'Apply Link'
                   ])

ua = faker.Faker().firefox()
head = {
    'User-Agent': ua,
    'Accept': '*/*',
    'Content-Type': 'application/json',
    }
site = 'https://www.accenture.com/api/sitecore/JobSearch/FindJobs'

t = "[{\"metadatafieldname\": \"skill\",\"items\":[]},{\"metadatafieldname\": \"location\",\"items\": []},{\"metadatafieldname\": \"postedDate\",\"items\": []},{\"metadatafieldname\": \"travelPercentage\",\"items\": []},{\"metadatafieldname\": \"jobTypeDescription\",\"items\": []},{\"metadatafieldname\": \"businessArea\",\"items\": []},{\"metadatafieldname\": \"specialization\",\"items\": []},{\"metadatafieldname\": \"workforceEntity\",\"items\": []},{\"metadatafieldname\": \"yearsOfExperience\",\"items\": []}]"
payload = {
    "f": 1,
    "s": 1000,
    "k": "",
    "lang": "en",
    "cs": "in-en",
    "df": t,
    "c": "India",
    "sf": 1,
    "syn": False,
    "isPk": False,
    "wordDistance": 0,
    "userId": ""
}

res = requests.post(url=site, data=json.dumps(payload), headers=head)
data = json.loads(res.text)

for i in data['documents']:
    l = [
        i['title'],
        ' '.join(i['location']),
        i['country'],
        i['feedExperienceLevel'],
        i['skill'],
        i['businessArea'],
        i['id'],
        i['requisitionId'],
        i['postedDate'],
        i['internalReferURL'],
    ]

    csvwriter.writerow(l)
    l.clear()

csvfile.close()
