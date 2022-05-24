import requests
import faker
import csv

from bs4 import BeautifulSoup

csvfile = open('details.csv', 'w', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['Title', 'Company Name', 'Job Type', 'Locations', 'Apply link', 'Job ID'])

ua = faker.Faker().firefox()
site = 'https://usijobs.deloitte.com/careersUSI/SearchJobsAJAX'
head = {'User-Agent': ua}

l = []
c = 1
for i in range(0, 151, 10):
    query = {
        's': 1,
        'jobOffset': i
    }
    res = requests.get(url=site, headers=head, params=query)

    soup = BeautifulSoup(res.text, 'html.parser')

    jobs = soup.find_all(name='article', class_='article--result opacity--0')

    for i in jobs:
        l.append(i.find('a').text.strip())
        l.append(i.find(name='div', class_='article__header__text__subtitle').text.split('|')[2].strip())
        job_link = i.find('a').get('href').strip()

        res = requests.get(url=job_link, headers=head)
        soup = BeautifulSoup(res.text, 'html.parser')
        basic_details = soup.find(name='article', class_='article article--details article--grow')

        l.append(' '.join(basic_details.find(name='div', class_='article__header__text__subtitle').text.split()))
        l.append(basic_details.find(name='div', class_='article__header--locations').text.strip())
        apply_link = soup.find(name='a', class_='button button--default').get('href')
        l.append(apply_link)
        l.append(apply_link.split('=')[-1])

        csvwriter.writerow(l)
        l.clear()

        print(c, 'done')
        c += 1

csvfile.close()
