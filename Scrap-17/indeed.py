import time
import json
import openpyxl
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
# driver.maximize_window()

driver.get("https://secure.indeed.com/auth")

time.sleep(5)

with open(file='login.json') as file:
    data = json.load(file)
    for j in data['login']:
        if j['name'] == 'Indeed':
            username, password = j['user_id'], j['password']
            break

def check_captcha():
    e = p = False
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form[1]/div[2]/div/iframe')
    except NoSuchElementException:
        e = False
    else:
        e = True

    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form[1]/div[2]/div/iframe')
    except NoSuchElementException:
        p = False
    else:
        p = True

    return e or p

def fill_email():
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div/span/input').clear()
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div/span/input').send_keys(username)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/button').click()
    time.sleep(15)

def fill_password():
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div[1]/span/input').clear()
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div[1]/span/input').send_keys(password)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/button').click()
    time.sleep(15)

# email
if check_captcha():
    print(56, 'email+captcha')
    fill_email()
    time.sleep(20)
else:
    print(60, 'only email')
    fill_email()

if check_captcha():
    print(64, 'email+captcha')
    fill_email()
    time.sleep(20)

# password
if check_captcha():
    print(70, 'password+captcha')
    fill_password()
    time.sleep(20)
else:
    print(74, 'only password')
    fill_password()

if check_captcha():
    print(78, 'password+captcha')
    fill_password()
    time.sleep(20)

# verification code
try:
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div[1]/div/span/input')
except:
    print('[+] No code asked...')
else:
    code = int(input('Enter code:\n'))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div[1]/div/span/input').send_keys(code)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/button').click()
'''
time.sleep(2)

# Post a job
driver.find_element(By.XPATH, '/html/body/nav/div[2]/div/div[2]/div[3]/div[2]/div/a').click()

time.sleep(2)

# Job details

# Job title
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[3]/div/div/div[1]/div/div/div/div/span/input').send_keys('Python Intern')

# Where will an employee report to work?
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/fieldset/label[2]').click()

time.sleep(1)

# Where would you like to advertise this job?
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')

# save and continue
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[6]/div/div/div[1]/div[2]/div[2]/button').click()

driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div/form/div/div[4]/div[4]/div/div/div/div/div/div/span/input').send_keys('Jabalpur, Madhya Pradesh')
'''


driver.quit()
