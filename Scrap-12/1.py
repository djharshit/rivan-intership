import requests
from bs4 import BeautifulSoup

site = 'https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid'
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.01) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/58.0.876.0 Safari/535.2'
}

res = requests.get(url=site, headers=head)
soup = BeautifulSoup(markup=res.text, features='html.parser')

x = soup.find(name='table').find_all(name='tr')

c = 1
for i in x:
    y = i.find_all(name='td')
    if len(y) != 0:
        print(y[0].text)
        print(y[1].text)
        print(y[2].text)
        print(c)
        c += 1
