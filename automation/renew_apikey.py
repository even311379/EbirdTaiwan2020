from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re

import passwords

driver = webdriver.Firefox()

driver.get('https://secure.birds.cornell.edu/cassso/login?')
ele_n = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))

# ele_n = driver.find_element_by_name('username')
ele_p = driver.find_element_by_name('password')
ele_submit = driver.find_element_by_id('form-submit')
ele_n.send_keys(passwords.ebird_account)
ele_p.send_keys(passwords.ebird_pass)

ele_submit.click()

driver.get('https://ebird.org/api/keygen')

htmltext = driver.page_source
driver.close()

if '密碼是' in htmltext:
    new_apikey = re.findall('碼是: (.*?)。將', htmltext)[0]
else:
    new_apikey = re.findall(r'PI Key is: (.*?)\.', htmltext)[0]


with open('automation/passwords.py', 'r') as f:
    old_password_file = f.read()

old_password_file = re.sub("ebird_api_key = '(.*?)'", f"ebird_api_key = '{new_apikey}'", old_password_file)

with open('automation/passwords.py', 'w+') as f:
    f.write(old_password_file)

