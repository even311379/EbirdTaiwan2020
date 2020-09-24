#feature test for ebird api
# Can I get access to what I want...

from ebird.api import Client
import time
import datetime

api_key = 'o1rng64r9e2b'
locale = 'zh'
client = Client(api_key, locale)

records = client.get_visits('TW', date=datetime.date.today())


region_codes = [
    'TW-TPE', #台北
    'TW-TPQ', #新北
    'TW-TAO', #桃園
    'TW-HSQ', #新竹
    'TW-MIA', #苗栗
    'TW-TXG', #台中
    'TW-CHA', #彰化
    'TW-NAN', #南投
    'TW-YUN', #雲林
    'TW-CYQ', #嘉義
    'TW-TNN', #台南
    'TW-KHH', #高雄
    'TW-PIF', #屏東
    'TW-TTT', #台東
    'TW-HUA', #雲林
    'TW-ILA', #宜蘭
    'TW-PEN', #澎湖
    'TW-KIN', #金門
    'TW-LIE', #連江
]

'''
records = client.get_observations(region_codes[6])

print(len(records))
print('********************')
print(records[0])
print(f'Check list: {records[0]["subId"]}')
print('*****************************************************')
checklist = client.get_checklist(records[0]['subId'])
# time.sleep(3)
print(checklist)
for k in checklist:
    print(k)

print('*****************************************************')
print('Can "get_visits" give me eaiser data to parse?')
'''
# records = client.get_visits(region_codes[6], date=datetime.date.today()-datetime.timedelta(days=1))

# hooray~~ I can use 'TW'
'''
records = client.get_visits('TW', date=datetime.date.today()-datetime.timedelta(days=1))
print(records)
print('********************TODAY*********************************')
records = client.get_visits('TW', date=datetime.date.today())
print(records[0])
print(records[1])
'''
# import pandas as pd

# birdcode_ref = pd.read_csv('../helper_files/eBird_Taxonomy_v2019.csv')
# birdcname_ref = pd.read_csv('')


checklist0 = client.get_checklist('S72361033')
checklist1 = client.get_checklist('S72339493')
print('**********************')
for i in checklist0:
    print(i)
print('**********************')
print(checklist0)

# ask the day question
'''
upload data time and obs data time?

'''
