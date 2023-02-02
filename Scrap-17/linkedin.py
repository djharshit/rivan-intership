import time
import json
# import excel_work

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


driver = webdriver.Chrome()
# driver.maximize_window()

driver.get('https://www.linkedin.com/uas/login')

time.sleep(2)

username = 'greymatter@telegmail.com'
password = 'fVy@Nr*Kf6,r5vA'

driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input').send_keys(username)
driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/form/div[2]/input').send_keys(password)
driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/form/div[3]/button').click()
time.sleep(1)
print(25)

# verification code
code = int(input('Enter code:\n'))
driver.find_element(By.XPATH, '/html/body/div/main/form/div[1]/input[16]').send_keys(code)
driver.find_element(By.XPATH, '/html/body/div/main/form/div[2]/button').click()
time.sleep(2)


# Start a post
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

driver.quit()
