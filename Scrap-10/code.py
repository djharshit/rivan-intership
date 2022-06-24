import csv
import json
import faker
import requests

csvfile = open('details.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile)
csvwriter.writerow([
                   'Title', 'ID', 'Job Code', 'Job Type', 'Opening',
                   'Experience', 'Qualification', 'Language',
                   'Location', 'Description', 'Apply Link'
                   ])

ua = faker.Faker().firefox()
head = {'User-Agent': ua}
site = 'https://radixweb.com/payload/current-openings/4-joblisting.json'

res = requests.get(url=site, headers=head)
data = json.loads(res.text)

for i in data['dynamicResult']:
    t = i['NavURL'].split('/')[-1]
    site = f'https://radixweb.com/payload/current-openings/{t}/{t}.json'
    res = requests.get(url=site, headers=head)

    data = eval(res.text, {'true': True}, {})[1][0]
    l = [
        data['JobTitle'],
        data['id'],
        data['JobCode'],
        data['JobType'],
        data['Opening'],
        data['Experience'],
        data['Qualification'],
        data['Language'],
        data['Location']
    ]
    try:
        l.append(data['ShortText'])
    except KeyError:
        l.append(None)
    try:
        e_mail = data['TurboEmail']
    except KeyError:
        e_mail = 'resumes@radixweb.com'
    l.append(f"https://radixweb.com/careerform-experience?job_code={data['JobCode']}&subject={data['JobTitle'].replace(' ', '+')}&emailid={m}")

    csvwriter.writerow(l)
    l.clear()

csvfile.close()
