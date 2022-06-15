import requests
import faker
import csv

from bs4 import BeautifulSoup

csvfile = open('details.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['Title', 'Location', 'Additional Location', 'Date',
                    'Apply Link', 'JobID'])

l = []
ua = faker.Faker().firefox()
site = 'https://careers.mcafee.com/search-jobs/results'
head = {'User-Agent': ua}

for i in range(1, 11):
    query = {
        'CurrentPage': i,
        'RecordsPerPage': 15,
        'Keywords': 'ALL',
        'SearchResultsModuleName': 'Search Results'
    }
    res = requests.get(url=site, headers=head, params=query)
    soup = BeautifulSoup(res.json()['results'], 'html.parser')
    jobs = soup.find(name='section', id='search-results-list').find_all(name='li')

    for i in jobs:
        l.append(i.a.h2.text)

        x = i.find_all('span')
        if len(x) == 3:
            l.append(x[0].text[18:])
            l.append(x[1].text[24:])
            l.append(x[2].text)
        else:
            l.append(x[0].text[18:])
            l.append(None)
            l.append(x[1].text)

        job_link = 'https://careers.mcafee.com' + i.a.get('href')

        res = requests.get(url=job_link, headers=head)
        soup = BeautifulSoup(res.text, 'html.parser')
        jobs = soup.find(name='section', class_='job-description')

        apply_link = jobs.find(name='a', class_='button job-apply top')
        l.append(apply_link.get('href'))
        job_id = jobs.find(name='span', class_='job-id job-info')
        l.append(job_id.text[8:])
        # job_desc = jobs.find(name='div', class_='ats-description').text.split(':')
        # job_overview = job_desc[1][:-14]
        # l.append(job_overview)
        # job_about = job_desc[2][:-9]
        # l.append(job_about)

        csvwriter.writerow(l)
        l.clear()

csvfile.close()
