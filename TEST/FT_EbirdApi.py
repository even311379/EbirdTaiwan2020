#feature test for ebird api
# Can I get access to what I want...

from ebird.api import get_observations, get_checklist

api_key = 'o1rng64r9e2b'

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

records = get_observations(api_key, region_codes[6], back=3)

print(len(records))
print('********************')
r0 = records[0]
print(f'Check list: {r0["subId"]}')
print('*****************************************************')
checklist = get_checklist(api_key, r0['subId'])
print(checklist)
