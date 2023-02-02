import csv
import requests
from bs4 import BeautifulSoup

csvfile = open('details.csv', 'w', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['Company Name', 'Address'])

for page in range(1, 11):
    response = requests.get(url=f'https://www.justdial.com/Mumbai/Toy-Distributors/nct-10490314/page-{page}',
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})

    soup = BeautifulSoup(response.text, 'html.parser')
    x = soup.find('section', class_='rslwrp').find_all('li', class_='cntanr')

    for i in x:
        name = i.find('h2', class_='store-name').text.strip()
        add = i.find('p', class_='address-info tme_adrssec').find('span', class_='cont_fl_addr').text.strip()

        csvwriter.writerow([name, add])

csvfile.close()
