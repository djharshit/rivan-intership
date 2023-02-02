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

driver.get('https://angel.co/login')

time.sleep(2)

with open(file='login.json') as file:
    data = json.load(file)
    for j in data['login']:
        if j['name'] == 'Indeed':
            username, password = j['user_id'], j['password']
            break

def captcha_login():
    pass

def account_login():
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[2]/div[3]/div[1]/form/input[4]').send_keys(username)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[2]/div[3]/div[1]/form/div[1]/input').send_keys(password)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[2]/div[3]/div[1]/form/div[2]/input').click()

try:
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[2]/div[3]/div[1]/form/input[4]')
    print(36)
except NoSuchElementException:
    # try:
    #     driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div[2]/p')
    # else:
    print('[+] Fill the captcha...')
    time.sleep(60)
    print(43)

    try:
        print(46)
        driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div')

    except NoSuchElementException:
        print(49)
        # account_login()
    else:
        print('[+] Your account is blocked..')

else:
    print(55)
    account_login()
    time.sleep(60)



time.sleep(60)
print(60)
'''
# verification code
code = int(input('Enter code:\n'))
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/div[1]/div/span/input').send_keys(code)
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/div[2]/div/form/button').click()
time.sleep(2)


# Start a post
https://angel.co/recruit/jobs/new
driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div[1]/div/div[1]/button').click()
time.sleep(3)
print(37)
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/span[4]/button').click()
time.sleep(3)
print(40)
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/fieldset/ul/li[5]/button').click()
time.sleep(3)
print(43)

# Job details

# Job title
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/input').send_keys('Python Intern')
# Workplace type
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[1]/div/div[3]/div/button').click()
# Job type
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[1]/div/div[5]/div[1]/div/input').send_keys('India')
# Next
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div/div/button[2]').click()
time.sleep(5)

# Description
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[1]/div[1]/section[1]/textarea').send_keys('Good knowlegde')
# Next
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div/button[2]').click()
time.sleep(5)

# Post
driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div/div[2]/div[2]/div[4]/button').click()
'''
driver.quit()
