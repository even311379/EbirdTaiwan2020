'''
Data pipeline for autumn challenge app

every hour to visit ebird api for all taiwan data
'''

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
logger = logging.getLogger('AutumnChanllenge')
# setup access to django db
import sys
import os
import django
from django.conf import settings
sys.path.append(os.path.abspath('ebirdtaiwan'))

from ebirdtaiwan.settings.base import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from fall.models import AutumnChanllengeData

import time
import pandas as pd
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import nearest_points

towns_polygons = {}
with open('../helper_files/TaiwanCounties.geojson') as f:
    raw_json = json.load(f)

for i in raw_json['features']:
    town_name = i['properties']['COUNTYNAME'] + i['properties']['TOWNNAME']
    towns_polygons[town_name] = i['geometry']['coordinates']
    # a town could have multiple polygons...離島之類的

from math import sin, cos, sqrt, atan2, radians

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


region_codes = {
    'TW-TPE' : '台北',
    'TW-KEE' : '基隆',
    'TW-TPQ' : '新北',
    'TW-TAO' : '桃園',
    'TW-HSQ' : '新竹',
    'TW-HSZ' : '新竹市',
    'TW-MIA' : '苗栗',
    'TW-TXG' : '台中',
    'TW-CHA' : '彰化',
    'TW-NAN' : '南投',
    'TW-YUN' : '雲林',
    'TW-CYQ' : '嘉義縣',
    'TW-CYI' : '嘉義市',
    'TW-TNN' : '台南',
    'TW-KHH' : '高雄',
    'TW-PIF' : '屏東',
    'TW-TTT' : '台東',
    'TW-HUA' : '花蓮',
    'TW-ILA' : '宜蘭',
    'TW-PEN' : '澎湖',
    'TW-KIN' : '金門',
    'TW-LIE' : '連江',
}


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

def UpdateDataFromEbirdApi(target_date):
    logger.info(f'Start to collect new data! 10/{target_date.day}')
    scraped_Ids = AutumnChanllengeData.objects.values_list('checklist_id', flat=True)
    api_data = []
    max_retry = 10
    for k in region_codes:
        api_requesting = True
        api_retry = 0
        while api_requesting:
            try:
                temp = client.get_visits(k, date = target_date)
                api_requesting = False
            except Exception as e:
                if api_retry > max_retry:
                    logger.error(f'Reached max api retry!!, cancel scraping {target_date}')
                    return
                api_retry += 1
                logger.error(f'ebird api faced error {e} ({k})({target_date}) Retry: {api_retry}')
                time.sleep(5)
            
        api_data += temp
        time.sleep(0.5)
        if len(temp) > 190:
            logger.warning(f'{target_date}/{region_codes[k]} could have more than 200 records!')
    N = 0
    for l in api_data:
        cid = l['subId']
        if cid not in scraped_Ids:
            N+=1
            api_requesting = True
            api_retry = 0
            while api_requesting:
                try:
                    obs = client.get_checklist(l['subId'])
                    api_requesting = False
                except Exception as e:
                    api_retry += 1
                    logger.error(f"ebird api faced error {e} {l['subId']} Retry: {api_retry}")
                    time.sleep(5)
                    if api_retry > max_retry:
                        logger.error(f'Reached max retry!! cancel scraping {target_date}')
                        return
            
            '''
            handle known issues
            '''
            if 'obsTime' not in l:
                logger.error(f"{l['subId']} is invalid due to lack of day time! (hours and minutes)")
                continue

            try:
                AutumnChanllengeData.objects.create(
                    checklist_id = l['subId'],
                    scrape_date = datetime.date.today(),
                    survey_datetime = datetime.datetime.strptime(l['obsDt'] + ' ' + l['obsTime'], '%d %b %Y %H:%M'),
                    creator = l['userDisplayName'],
                    latitude = l['loc']['latitude'],
                    longitude = l['loc']['longitude'],
                    county = GetCountyByCoord(l['loc']['latitude'], l['loc']['longitude']),
                    is_valid = bool(obs['obs'])
                )
            except Exception as e:
                logger.error(f'!!!{l}: {e}!!!')                
    logger.info(f'Add {N} new checklists!')


def RescrapeFromFirstDay():
    logger.info('start to rescrap all data from 10/1 to now!')
    now = datetime.datetime.now()
    for d in range(1, now.day):
        UpdateDataFromEbirdApi(datetime.date(2020,10,d))
        time.sleep(3)


if __name__ == '__main__':
    RescrapeFromFirstDay()
    while True:        
        now = datetime.datetime.now()
        if now.minute == 0:
            if now.hour %3 == 0:
                UpdateDataFromEbirdApi(datetime.date.today())
            if now.hour == 6:
                logger.info('start to rescrape 3 days data')
                if now.date == datetime.date(2020,10,1):
                    pass
                elif now.date == datetime.date(2020,10,2):
                    UpdateDataFromEbirdApi(datetime.date.today() - datetime.timedelta(days=1))
                else:
                    UpdateDataFromEbirdApi(datetime.date.today() - datetime.timedelta(days=1))
                    UpdateDataFromEbirdApi(datetime.date.today() - datetime.timedelta(days=1))
                if now.day % 3 == 0:
                    RescrapeFromFirstDay()

        time.sleep(60)

    

'''
ISSUES:

(1) 使用者過了好幾天才上傳之前的資料，那我就必須去重複的抓好幾天前的資料？
     平常抓3天內，一週一次重抓這個月內？
(2) 分享清單問題，會不會重複？  有沒有辦法區別？

'''
