import requests
import faker
import csv

from bs4 import BeautifulSoup

csvfile = open('details.csv', 'w', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['Title', 'Locations', 'Date', 'Country', 'JobID', 'Function', 'Link'])

ua = faker.Faker().firefox()
site = 'https://jobs.epicor.com/careers/SearchJobs/'
head = {'User-Agent': ua}

l = []
c = 1
for i in range(0, 271, 6):
    query = {
        'jobRecordsPerPage': 6,
        'jobOffset': i
    }
    res = requests.get(url=site, headers=head, params=query)

    soup = BeautifulSoup(res.text, 'html.parser')
    jobs = soup.find_all(name='article', class_='article article--result')

    for i in jobs:
        print(c)
        l.append(i.find('a').text.strip())
        i_site = i.find('a').get('href')

        res = requests.get(url=i_site, headers=head)

        soup = BeautifulSoup(res.text, 'html.parser')
        data = soup.find('div', class_='section__content').find_all(name='div', class_='article__content__view__field__value')

        for i in data[:-1]:
            l.append(i.text.strip())
        l.append(soup.find('a', class_='button button--primary--two').get('href'))

        csvwriter.writerow(l)
        l.clear()
        c += 1

csvfile.close()
