'''

(1) Check if how many data I've scraped before are still there
(2) If I can find some way to match those missing ones


'''
import eb_passwords
from ebird.api import Client, get_visits
import datetime

api_key = eb_passwords.ebird_api_key
locale = 'zh'
client = Client(api_key, locale)

import sys
import os
import django
from django.conf import settings
sys.path.append(os.path.abspath('ebirdtaiwan'))
from ebirdtaiwan.settings.base import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from fall.models import AutumnChanllengeData

#################################
####  TEST 1 ####################
###############################

'''
today = datetime.date.today()
db_data = AutumnChanllengeData.objects.all()

for d in range(1, today.day+1):
    D = datetime.date(2018,10,d)
    print('*****************************')
    print(D)
    api_data = client.get_visits('TW', date=D)
    db_checklists = AutumnChanllengeData.objects.filter(survey_datetime__day=D.day).values_list('checklist_id', flat=True)
    api_checklists = []
    for data in api_data:
        api_checklists.append(data['subID'])
    n_db_missing = 0
    for cl in api_checklists:
        if cl not in db_checklists:
            print(f'Missing checklist in db: {cl}')
            n_db_missing += 1
    n_api_missing = 0
    for cl in db_checklists:
        if cl not in api_checklists:
            print(f'Missing checklist in api: {cl}')
            n_api_missing += 1
    print(f'Total data in api: {len(api_checklists)}')
    print(f'Total data in DB: {len(db_checklists)}')
    print(f'data in api but missing in db: {n_db_missing}')
    print(f'data in db but missing in api: {n_api_missing}')

'''


'''
lots of data disappeared in ebird api from get_visits... why?
(1) cid is changed?
(2) it is just removed?

use other way to check if it is still there!?

'''


'''
maybe.... the maximun length of data return is fixed...
maybe use smaller region unit and repeat can fix the issue...


'''

############################################################
#################### TEST 2 #############################
##########################################################

'''

region_codes = {
    'TW-TPE' : '台北',
    'TW-TPQ' : '新北',
    'TW-TAO' : '桃園',
    'TW-HSQ' : '新竹',
    'TW-MIA' : '苗栗',
    'TW-TXG' : '台中',
    'TW-CHA' : '彰化',
    'TW-NAN' : '南投',
    'TW-YUN' : '雲林',
    'TW-CYQ' : '嘉義縣',
    'TW-TNN' : '台南',
    'TW-KHH' : '高雄',
    'TW-PIF' : '屏東',
    'TW-TTT' : '台東',
    'TW-HUA' : '雲林',
    'TW-ILA' : '宜蘭',
    'TW-PEN' : '澎湖',
    'TW-KIN' : '金門',
    'TW-LIE' : '連江',
    'TW-CYI' : '嘉義市',
    'TW-KEE' : '基隆',
}

nd = 0
for k in region_codes:
    data = client.get_visits(k, date = datetime.date(2018,10,1))
    nd += len(data)

twdata = client.get_visits('TW', date = datetime.date(2018,10,1))
print(f'every county {nd} VS TW {len(twdata)}')
records = get_visits(api_key, 'TW', '2018-10-01', max_results=200)
print(f'another way to get TW data: {len(records)}')

'''


records = get_visits(api_key, 'TW', '2018-10-01', max_results=200)
print(f'2018-10-01: {len(records)}')

records = get_visits(api_key, 'TW', '2018-10-02', max_results=200)
print(f'2018-10-02: {len(records)}')

records = get_visits(api_key, 'TW', '2018-10-03', max_results=200)
print(f'2018-10-03: {len(records)}')

records = get_visits(api_key, 'TW', '2018-10-04', max_results=200)
print(f'2018-10-04: {len(records)}')

records = get_visits(api_key, 'TW', '2018-10-05', max_results=200)
print(f'2018-10-05: {len(records)}')

records = get_visits(api_key, 'TW', '2018-9-01', max_results=200)
print(f'2018-9-01: {len(records)}')

records = get_visits(api_key, 'TW', '2018-9-02', max_results=200)
print(f'2018-9-02: {len(records)}')

records = get_visits(api_key, 'TW', '2018-9-03', max_results=200)
print(f'2018-9-03: {len(records)}')

records = get_visits(api_key, 'TW', '2018-9-04', max_results=200)
print(f'2018-9-04: {len(records)}')

records = get_visits(api_key, 'TW', '2018-9-05', max_results=200)
print(f'2018-9-05: {len(records)}')


records = get_visits(api_key, 'TW', '2018-8-01', max_results=200)
print(f'2018-8-01: {len(records)}')

records = get_visits(api_key, 'TW', '2018-8-02', max_results=200)
print(f'2018-8-02: {len(records)}')

records = get_visits(api_key, 'TW', '2018-8-03', max_results=200)
print(f'2018-8-03: {len(records)}')

records = get_visits(api_key, 'TW', '2018-8-04', max_results=200)
print(f'2018-8-04: {len(records)}')

records = get_visits(api_key, 'TW', '2018-8-05', max_results=200)
print(f'2018-8-05: {len(records)}')