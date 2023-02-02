from csv import writer
import urllib.request
from bs4 import BeautifulSoup

class JustDail:
    def __init__(self):
        with open('JustDialfinal12.csv', 'w', encoding='utf8', newline='') as f:
            thewriter = writer(f)
            header = ['Name', 'Phone Number', 'Address']
            thewriter.writerow(header)
            self.name, self.address, self.phone = [], [], []
    def detailsscrap(self,id_no):
        req = urllib.request.Request(f'https://www.justdial.com/Hyderabad/Eye-Hospitals/nct-10196517/page-{id_no}',headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"})
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page.read(), "html.parser")
        x = soup.find_all('style', type='text/css')
        t = (str(x[-1].text).split('.icon-'))
        count = 0
        dic = {}
        for i in t[1:]:
            dic[i[:3]] = str(count)
            count += 1
        v = soup.find_all('li', class_='cntanr')
        for i in v:
            self.name.append(i.find('img').get('alt').split(' in ')[0])
            self.address.append(i.find('span', class_='cont_fl_addr').text)
            content = i.find('p', class_='contact-info')
            try:
                numberTags = (content.find('a'))
                number = []
                if "+(" in numberTags:

                    list = (numberTags.find_all('span'))
                    count = 0
                    number.append(" +(")
                    for i in range(len(list)):
                        count += 1
                        if count == 3:
                            number.append(')-')
                        number.append(dic[list[i].get('class')[1].split('-')[1]])
                    self.phone.append(''.join(number))
                else:
                    list = (numberTags.find_all('span'))
                    for i in range(len(list)):
                        number.append(dic[list[i].get('class')[1].split('-')[1]])
                    self.phone.append(''.join(number))
            except:
                self.phone.append("")
    def exctractData(self,totoal_details):
        for i in range(totoal_details):
            with open('JustDialfinal12.csv', 'a', encoding='utf8', newline='') as f:
                thewriter = writer(f)
                row = (self.name[i],self.phone[i],self.address[i])
                thewriter.writerow(row)

obj = JustDail()
for i in range(1,11):
    obj.detailsscrap(i)
obj.exctractData(len(obj.name))
