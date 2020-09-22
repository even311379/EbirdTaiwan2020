# setup selenium
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re 

profile = webdriver.FirefoxProfile()
options = Options()
options.headless = True
profile.set_preference("dom.webnotifications.enabled", False)  # Finally, turned off webnotifications...


#####################################
profile.set_preference("intl.accept_languages","zh-tw") # can I force selenium "zh-tw" by this option
######################################

profile.update_preferences()    
driver = webdriver.Firefox(firefox_profile=profile, options=options)

# setup ebird api
from ebird.api import Client
import datetime

api_key = 'o1rng64r9e2b'
locale = 'zh'
client = Client(api_key, locale)

# setup logger
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(name)s - %(asctime)s - %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='scraper.log'
)
logger = logging.getLogger('Scraper')

''' # test headless
logger.info('test headless')
driver.get('https://stackoverflow.com/questions/46753393/how-to-make-firefox-headless-programmatically-in-selenium-with-python')
logger.info(f'success!? : {driver.title}')
driver.close()
'''

# setup access to django db
import sys
import os
import django
from django.conf import settings
sys.path.append(os.path.abspath('ebirdtaiwan'))

from ebirdtaiwan.settings.base import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from fall.models import Survey, SurveyObs

logger.info('Scraper started!')

account = 'ET黑面琵鷺隊'
password ='201910BFS'

driver.get('https://secure.birds.cornell.edu/cassso/login?')
ele_submit = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "form-submit")))
ele_n = driver.find_element_by_name('username')
ele_p = driver.find_element_by_name('password')
ele_n.send_keys(account)
ele_p.send_keys(password)
ele_submit.click()
driver.get('https://ebird.org/shared')
time.sleep(5)
btns = [b for b in driver.find_elements_by_tag_name('button') if b.text == 'Accept' or b.text == 'Keep']

n_btn_clicked = 0
max_allowed_click_times = 200
while btns:
    btns[0].click
    time.sleep(3)
    btns = [b for b in driver.find_elements_by_tag_name('button') if b.text == 'Accept' or b.text == 'Keep']
    n_btn_clicked += 1
    if n_btn_clicked >= max_allowed_click_times:
        logger.error('Reached maxed allowed btn clicked times, could trigger infinite loop')
        break

if n_btn_clicked > 0: 
    logger.info(f'{account} accept {n_btn_clicked} new checklist!')

# get all checklist url and add new ones to database

htmltext = driver.page_source

# only take five for test purpose
all_checklist_id = re.findall('/checklist/(.*?)"', htmltext)[7:52]
all_creators = re.findall('"owner" class="dataCell">(.*?)</td>', htmltext)[7:52]

db_checklists = Survey.objects.values_list('checklist_id', flat=True)

for i, c in zip(all_checklist_id, all_creators):
    if i not in db_checklists:
        api_data = client.get_checklist(i)
        driver.get('https://ebird.org/checklist/'+i)
        htmltext = driver.page_source

        # get species names
        S = re.findall('Heading-main\".*?>(.*?)</span',htmltext)[4:]
        # get species amounts
        N = [-1 if n == 'X' else int(n) for n in re.findall('<span>([X|\d]\d*?)</span>',htmltext)]

        gps_loc = re.findall('"https://www.google.com/maps/search.*query=(.*?)"', htmltext)[0]
        NewSurvey = Survey(
            team = '黑面琵鷺隊',
            checklist_id=i,
            creator=c,
            survey_datetime = datetime.datetime.strptime(api_data['obsDt'], '%Y-%m-%d %H:%M'),
            latitude=float(gps_loc.split(',')[0]),
            longitude=float(gps_loc.split(',')[0]),
            region_code = api_data['subnational1Code'],
            is_valid = -1 in N or api_data['durationHrs'] < 0.084
        )
        NewSurvey.save()

        if not N or not S or len(N) != len(S):
            logger.warning(f'checklist: {i} contains no data!')
            break

        # fix some special case?
        if 'eBird' in S[0]:
            S = S[2:]
        if 'Checklist flagged' in S:  
            S.remove('Checklist flagged')

        for s,n in zip(S, N):
            SurveyObs.objects.create(
                survey=Survey.objects.get(checklist_id=i),
                species_name=s,
                amount=n
            )

        time.sleep(2)        
# 

driver.close()
logger.info('Scraper finished!')