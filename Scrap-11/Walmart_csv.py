import requests
import csv

csvfile = open('details.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile)
csvwriter.writerow([
                   'Title', 'Job Code', 'Job Function', 'Qualifications',
                   'Min Qualifications', 'Min Experience', 'Max Experience',
                   'City', 'State', 'Country', 'Apply Link'
                   ])

site = 'https://one.walmart.com/bin/careers/onprem/elsearch.json'

head = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:1.9.6.20) Gecko/2017-04-09 14:36:31 Firefox/11.0'
}

query = {
    'min_exp': 0,
    'max_exp': 10,
    'data_source': 'in',
    'country': 'india',
    'keyword': None,
    'page': 1,
    'results_per_Page': 100,
    'sort_by': 'SCORE',
    'gtsCareer': True
}
response = requests.get(url=site, headers=head, params=query)

data = response.json()
print('Total jobs are', data['numFound'])

l = []
for i in data['results']:
    l.append(i['title'])
    l.append(i['job_code'])
    try:
        l.append(i['job_function'])
    except KeyError:
        l.append(None)
    l.append(i['preferred_qualifications_en'])
    l.append(i['min_qualifications_en'])
    l.append(i['min_experience'])
    l.append(i['max_experience'])
    l.append(i['city'])
    l.append(i['state'])
    l.append(i['country'])
    l.append(i['apply_link'])

    csvwriter.writerow(l)
    l.clear()

csvfile.close()
