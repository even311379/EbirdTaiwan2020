'''
Data pipeline for autumn challenge app

every hour to visit ebird api for all taiwan data
'''

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

towns_polygons = {}
with open('../helper_files/TaiwanCounties_simple.geojson') as f:
    raw_json = json.load(f)

for i in raw_json['features']:
    town_name = i['properties']['COUNTYNAME'] + i['properties']['TOWNNAME']
    towns_polygons[town_name] = i['geometry']['coordinates']
    # a town could have multiple polygons...離島之類的


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
            
    return '不在台灣啦!'

def UpdateDataFromEbirdApi():
    scraped_Ids = AutumnChanllengeData.objects.values_list('checklist_id', flat=True)
    checklists = client.get_visits('TW', date = datetime.date.today())
    for l in checklists:
        cid = l['subId']
        if cid not in scraped_Ids:
            obs = client.get_checklist(l['subId'])
            AutumnChanllengeData.objects.create(
                checklist_id = l['subId'],
                creator = l['userDisplayName'],
                latitude = l['latitude'],
                longitude = l['longitude'],
                county = GetCountyByCoord(l['latitude'], l['longitude']),
                is_valid = bool(obs['obs'])
            )






if __name__ == '__main__':
    # while True:
    #     if datetime.datetime.now().minute == 0:
    #         UpdateDataFromEbirdApi()
    #     time.sleep(60)

    print(GetCountyByCoord(24.669527, 121.725319))
    print(GetCountyByCoord(24.996413, 119.447619))
    print(GetCountyByCoord(25.118471, 119.373589))
    print(GetCountyByCoord(23.205872, 120.813756))
    
    

'''
ISSUES:

(1) 使用者過了好幾天才上傳之前的資料，那我就必須去重複的抓好幾天前的資料？
     平常抓3天內，一週一次重抓這個月內？
(2) 分享清單問題，會不會重複？  有沒有辦法區別？

'''