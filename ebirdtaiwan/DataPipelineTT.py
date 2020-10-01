'''
Data pipeline for three teams competition app

'''

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
profile.set_preference("intl.accept_languages","zh-tw")
profile.update_preferences()    
driver = webdriver.Firefox(firefox_profile=profile, options=options)

# setup ebird api
import eb_passwords
from ebird.api import Client
import datetime

api_key = eb_passwords.ebird_api_key
locale = 'zh'
client = Client(api_key, locale)

# setup logger
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(name)s - %(asctime)s - %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='DataPipeline.log'
)
logger = logging.getLogger('ThreeTeams')


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

import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import nearest_points
from math import sin, cos, sqrt, atan2, radians

towns_polygons = {}
with open('../helper_files/TaiwanCounties_simple.geojson') as f:
    raw_json = json.load(f)

for i in raw_json['features']:
    town_name = i['properties']['COUNTYNAME'] + i['properties']['TOWNNAME']
    towns_polygons[town_name] = i['geometry']['coordinates']

def great_circle_distance_on_earth(point1, point2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(point1.y)
    lon1 = radians(point1.x)
    lat2 = radians(point2.y)
    lon2 = radians(point2.x)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def GetCountyByCoord(lat, lon):
    point = Point(lon, lat)
    for town in towns_polygons:        
        for town_polygon in towns_polygons[town]:
            if len(town_polygon) == 1:
                polygon = Polygon(town_polygon[0])
            else:            
                polygon = Polygon(town_polygon)
            if polygon.contains(point):                
                return town

    logger.warning(f'Vague point detected! Start further algorithm to check its town ')
    
    for town in towns_polygons:
        for town_polygon in towns_polygons[town]:
            if len(town_polygon) == 1:
                polygon = Polygon(town_polygon[0])
            else:            
                polygon = Polygon(town_polygon)
            p1, _ = nearest_points(polygon, point)            
            if great_circle_distance_on_earth(point, p1) < 5: # distance to shore 5km?
                logger.info(f'Success detect its town as {town}!')
                return town
    logger.warning(f'Failed to detect town!')                
    return '不在台灣啦!'

def ScrapDataFromAccount(team_name, account, password):

    logger.info(f'Scraper started! ({team_name})')

    driver.get('https://secure.birds.cornell.edu/cassso/login?')
    ele_submit = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "form-submit")))
    ele_n = driver.find_element_by_name('username')
    ele_p = driver.find_element_by_name('password')
    ele_n.send_keys(account)
    ele_p.send_keys(password)
    ele_submit.click()
    driver.get('https://ebird.org/shared')
    time.sleep(5)
    btns = [b for b in driver.find_elements_by_tag_name('button') if b.text == '接受' or b.text == '保留']

    n_btn_clicked = 0
    max_allowed_click_times = 200
    while btns:
        btns[0].click()
        time.sleep(3)
        btns = [b for b in driver.find_elements_by_tag_name('button') if b.text == '接受' or b.text == '保留']
        n_btn_clicked += 1
        if n_btn_clicked >= max_allowed_click_times:
            logger.error('Reached maxed allowed btn clicked times, could trigger infinite loop')
            break

    if n_btn_clicked > 0: 
        logger.info(f'{account} accept {n_btn_clicked} new checklist!')

    # get all checklist url and add new ones to database

    htmltext = driver.page_source

    # only take five for test purpose
    all_checklist_id = re.findall('/checklist/(.*?)"', htmltext)
    all_creators = re.findall('"owner" class="dataCell">(.*?)</td>', htmltext)
    db_checklists = Survey.objects.values_list('checklist_id', flat=True)

    new = 0
    
    for i, c in zip(all_checklist_id, all_creators):
        if i not in db_checklists:
            valid = True            
            api_data = client.get_checklist(i)            
            if api_data['subnational1Code'] not in ['TW-TPE', 'TW-TPQ']:
                logger.warning(f'{c} shared a list({i}) not inside competition area!, save it as invalid data')
                valid = False                
            elif 'durationHrs' not in api_data:
                logger.warning(f'checklist: {i} contains no durationHrs!!?, save it as invalid data')
                valid = False            

            driver.get('https://ebird.org/checklist/'+i)
            htmltext = driver.page_source
            # get species names
            S = re.findall('Heading-main\".*?>(.*?)</span',htmltext)[4:]
            # get species amounts
            N = [-1 if n == 'X' else int(n) for n in re.findall(r'<span>([X|\d]\d*?)</span>',htmltext)]            
            gps_loc = re.findall('"https://www.google.com/maps/search.*query=(.*?)"', htmltext)[0]

            if valid:
                valid = -1 not in N and api_data['durationHrs'] > 0.084
            NewSurvey = Survey(
                scrape_date = datetime.date.today(),
                team = team_name,
                checklist_id=i,
                creator=c,
                survey_datetime = datetime.datetime.strptime(api_data['obsDt'], '%Y-%m-%d %H:%M'),
                latitude=float(gps_loc.split(',')[0]),
                longitude=float(gps_loc.split(',')[1]),
                county = GetCountyByCoord(float(gps_loc.split(',')[0]), float(gps_loc.split(',')[1])),
                is_valid = valid
            )
            NewSurvey.save()

            if not valid:
                time.sleep(1)
                continue

            new += 1
            # fix some special case?
            if 'eBird' in S[0]:
                S = S[2:]
            if 'Checklist flagged' in S:  
                S.remove('Checklist flagged')

            if not N or not S or len(N) != len(S):
                logger.warning(f'checklist: {i} contains no data!')
                continue

            for s,n in zip(S, N):
                SurveyObs.objects.create(
                    survey=Survey.objects.get(checklist_id=i),
                    species_name=s,
                    amount=n
                )
            time.sleep(1)        

    driver.close()
    logger.info(f'Scraper finished with {new} new checklist!')


if __name__ == '__main__':
    team_names = ['彩鷸隊', '家燕隊', '大冠鷲隊']
    accounts = [eb_passwords.team_left_account, eb_passwords.team_middle_account, eb_passwords.team_right_account]
    passes = [eb_passwords.team_left_password, eb_passwords.team_middle_password, eb_passwords.team_right_password]
    for name, account, password in zip(team_names, accounts, passes):
        ScrapDataFromAccount(name, account, password)  
    while True:
        if datetime.datetime.now().minute == 20 and datetime.datetime.now().hour % 3 == 1:            
            for name, account, password in zip(team_names, accounts, passes):
                ScrapDataFromAccount(name, account, password)                    

        time.sleep(60)
