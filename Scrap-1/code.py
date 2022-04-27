import re
import csv
import time
import mysql.connector
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions

con = mysql.connector.connect(host='sql6.freesqldatabase.com',
                              user='sql6483131',
                              password='DpIeCZkBCx',
                              port=3306,
                              database='sql6483131')

if con.is_connected():
    print('Connected')
else:
    print('Not connected')

cur = con.cursor()

driver = webdriver.Chrome()
driver.minimize_window()
driver.get('https://www.stfrancismedicalcenter.com/find-a-provider/')

first_driver = driver

time.sleep(3)
l = []

for pageno in range(1, 38):
    i = 1
    clients = driver.find_elements(by=By.XPATH, value='//li[@data-role="tr"]')

    for client in clients:
        print('\n', pageno, i)

        name = client.find_element(by=By.XPATH, value='.//div/meta[@itemprop="name"]').get_attribute('content')
        l.append(name)

        try:
            speciality = client.find_element(by=By.XPATH, value='.//div[@class="info"]/div/span').text
            l.append(speciality)
        except exceptions.NoSuchElementException:
            l.append(None)

        practice = client.find_element(by=By.XPATH, value='.//div/meta[@itemprop="legalName"]').get_attribute('content')
        if not practice:
            l.append(None)
        else:
            l.append(practice)

        address = client.find_element(by=By.XPATH, value='.//div/meta[@itemprop="streetAddress"]').get_attribute('content')
        l.append(address)

        city = client.find_element(by=By.XPATH, value='.//div/meta[@itemprop="addressLocality"]').get_attribute('content')
        l.append(city)

        state = client.find_element(by=By.XPATH, value='.//div/meta[@itemprop="addressRegion"]').get_attribute('content')
        l.append(state)

        pin_code = client.find_element(by=By.XPATH, value='.//div/meta[@itemprop="postalCode"]').get_attribute('content')
        l.append(pin_code)

        phone = client.find_element(by=By.XPATH, value='.//div/meta[@itemprop="telephone"]').get_attribute('content')
        l.append(phone)

        profile_url = client.find_element(by=By.XPATH, value='.//a').get_attribute('href')
        l.append(profile_url)

        page_name = re.sub(r'[\W]', '', profile_url)
        with open(f'new_html/{page_name}.html', 'w', encoding='utf-8') as file:
            file.write(requests.get(profile_url).text)

        pic_url = client.find_element(by=By.XPATH, value='.//img').get_attribute('src')
        # print(pic_url)
        with open(f'new_image/{page_name}.jpg', 'wb') as file:
            try:
                file.write(requests.get(pic_url).content)
            except:
                pass

        cur.execute('insert into selenium values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', l)
        con.commit()

        l.clear()

        i += 1

    driver.find_element(by=By.XPATH, value='//a[@class="next"]').click()
    time.sleep(3)

driver.quit()
con.close()
