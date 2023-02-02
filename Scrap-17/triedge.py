#!/usr/bin/python3

# ========== Importing the required modules ==========
import time
import json
import openpyxl
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# ========== Defining the variables ==========
parser = argparse.ArgumentParser(description='Script to automate the job posting in the triedge portal.')
parser.add_argument('file', metavar='<file>', type=str, help='The xlsx file name containing the details.')
args = parser.parse_args()

workbook = openpyxl.load_workbook(filename=args.file)
worksheet = workbook.active
i = 2

with open(file='login.json') as file:
    data = json.load(file)
    for j in data['login']:
        if j['name'] == 'TriEdge':
            username, password = j['username'], j['password']
            break

# ========== Create a new session ==========
driver = webdriver.Chrome()
# driver.maximize_window()

driver.get('https://triedge.in/')
time.sleep(3)

# ========== Login in the portal ==========
driver.find_element(By.XPATH, '/html/body/div[3]/header[1]/div/div[1]/div[2]/div/ul/li[3]/a').click()
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/form/fieldset/div[2]/div/div/input[1]').send_keys(username)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/form/fieldset/div[3]/div/div/input').send_keys(password)
driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/form/fieldset/div[6]/div[1]/button').click()
time.sleep(2)

while True:
    job_title = worksheet[f'A{i}'].value
    stipend = worksheet[f'B{i}'].value
    description = f"{worksheet[f'C{i}'].value}\n\nSkills required:\n{worksheet[f'D{i}'].value}"

    if job_title is None: break # All the jobs have been posted

    # ========== Create a new job posting ==========
    driver.get('https://posting.triedge.in/db/poshortdetailjobposting/')

    # ========== Fill information about the job ==========

    # Position title
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[1]/div/div/input[9]').send_keys(job_title)
    time.sleep(2)
    # Website url
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[5]/div/div/input').send_keys('https://www.rivan.in/')
    # Position type
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[7]/div/div/div[1]/div/label[1]').click()
    # Functional area
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[9]/div/div/div[1]/div/select')
    Select(sel).select_by_visible_text('Technology')
    # Work start date
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[11]/div/div/div[2]/div[1]/div/select')
    Select(sel).select_by_visible_text('Immediate')
    # Position duration
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[11]/div/div/div[1]/div/div[1]/input').send_keys(6)
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[11]/div/div/div[1]/div/div[2]/select')
    Select(sel).select_by_visible_text('Month(s)')
    # Workplace type
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[13]/div/div/div[1]/div/select')
    Select(sel).select_by_visible_text('Work from Home/ Virtual')
    # No. of positions
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[15]/div/div/div[1]/div/div[1]/div/input').send_keys(10)
    # Job role
    time.sleep(3)
    inside_frame = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[17]/div/div/div[2]/div/div/iframe')
    driver.switch_to.frame(inside_frame)
    elem = driver.find_element(By.XPATH, '/html/body/p')
    elem.send_keys(description)
    driver.switch_to.default_content()

    # driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[17]/div/div/div[2]/div/div/iframe').send_keys(2)
    # Preferred education level
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[19]/div/div[1]/div/span/select')
    Select(sel).select_by_visible_text('UG - Degree Course(s)')
    time.sleep(2)
    # Financial reward
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[21]/div/div/div[2]/div/select')
    Select(sel).select_by_visible_text('Paid- Fixed')
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[22]/div/div/div[2]/div[1]/input').send_keys(stipend)
    # Payable
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[22]/div/div/div[3]/div/select')
    Select(sel).select_by_visible_text('Monthly')
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[26]/div/div/div[2]/div/div/div/label[1]').click()

    time.sleep(2)

    # Finalise job description
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[34]/button').click()
    # Skip the assesement question
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div[2]/div/div/div/div[3]/button').click()

    # ========== Click the submit button for approval ==========
    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[13]/button').click()

    time.sleep(5)
    print('[+] Job successfully posted', job_title)
    time.sleep(10)

    i += 1

print('All jobs have been posted...now quit')

driver.quit()
