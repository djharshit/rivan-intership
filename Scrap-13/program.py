from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re

comp_name = []

with open('count.txt') as file: # Loading count
    count = int(file.read())

print('Starting from count', count)
    
with open (file='names.csv') as file:
    csvreader = csv.reader(file)
    for i in csvreader:           
        comp_name.append(i[1].replace(' ', '+').replace("'", '%27'))

del comp_name[0] # Delete heading row
comp_name = comp_name[count:] # Process remaining comp_name

head_row = ['Company', 'Email']

with open(file='email_all1.csv', mode='a', encoding='utf-8', newline='') as file:
    csvwriter = csv.writer(file)

    if count == 0:
        csvwriter.writerow(head_row)
    
    try:
        for search_key in comp_name:
            regex_email = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
            
            PATH = r'C:\Program Files (x86)\chromedriver\chromedriver.exe'
            driver = webdriver.Chrome(PATH)
            driver.get(f"https://www.google.com/search?q={search_key}&rlz=1C1UEAD_enIN977IN977&sxsrf=ALiCzsb4qTBI_amqsCcMrZTBJeBDqf_b5A%3A1664009966882&ei=7sYuY7TCNdr04-EP25yxgAc&oq=chrome+scraping+with+&gs_lp=Egdnd3Mtd2l6uAED-AEBKgIIADIFECEYoAEyBRAhGKABMgUQIRigATIFECEYoAHCAgoQABhHGNYEGLADwgIHECMY6gIYJ8ICBBAjGCfCAgQQABhDwgIIEC4Y1AIYkQLCAgUQLhiRAsICERAuGIAEGLEDGIMBGMcBGNEDwgIFEAAYgATCAgsQABiABBixAxiDAcICChAAGLEDGIMBGEPCAgUQABiRAsICBxAAGLEDGEPCAggQABiABBixA8ICCBAAGIAEGMkDwgIGEAAYHhgWwgIFEAAYhgOoAgqQBghIpa0BUNMMWOWcAXACeAHIAQCQAQSYAbQDoAG_LKoBCzAuMTQuMTAuMC4y4gMEIEEYAOIDBCBGGACIBgE&sclient=gws-wiz")
            
            # driver.implicitly_wait(0.5)
            
            searchstring = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='rcnt']"))).text
            driver.quit()

            match = re.findall(regex_email, searchstring)

            one_data = [str(search_key).replace('+', ' '), str(match)]
            csvwriter.writerow(one_data)

            count += 1
            
    except Exception as err:
        print('Error occured...saving count', err)

        with open('count.txt', 'w') as file: # Saving count in case of failure
            file.write(str(count))
