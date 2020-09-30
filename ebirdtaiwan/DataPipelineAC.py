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
with open('../helper_files/TaiwanCounties_simple.geojson') as f:
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
    logger.info(f'Start to collect new data!')
    scraped_Ids = AutumnChanllengeData.objects.values_list('checklist_id', flat=True)
    checklists = client.get_visits('TW', date = target_date)
    N = 0
    for l in checklists:
        cid = l['subId']
        if cid not in scraped_Ids:
            N+=1
            obs = client.get_checklist(l['subId'])
            
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





if __name__ == '__main__':
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
                if now.weekday() == 6:
                    logger.info('start to rescrape all data from 10/01 to now')
                    for i in range(1, now.day - 2):
                        UpdateDataFromEbirdApi(datetime.date(2020,10,i))
        time.sleep(60)

    # while True:
    #     if datetime.datetime.now().minute == 0:
    #         UpdateDataFromEbirdApi()
    #     time.sleep(60)


    # print(GetCountyByCoord(24.669527, 121.725319))
    # print(GetCountyByCoord(24.996413, 119.447619))
    # print(GetCountyByCoord(25.118471, 119.373589))
    # print(GetCountyByCoord(23.205872, 120.813756))
    
    

'''
ISSUES:

(1) 使用者過了好幾天才上傳之前的資料，那我就必須去重複的抓好幾天前的資料？
     平常抓3天內，一週一次重抓這個月內？
(2) 分享清單問題，會不會重複？  有沒有辦法區別？

'''