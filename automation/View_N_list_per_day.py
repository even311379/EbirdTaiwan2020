from ebird.api import Client
import time
import datetime

api_key = 'o1rng64r9e2b'
locale = 'zh'
client = Client(api_key, locale)

start_date = datetime.date(2020,9,5)

for i in range(15):
    print(start_date + datetime.timedelta(days=i))
    records = client.get_visits('TW', date=start_date + datetime.timedelta(days=i))
    print(f'have {len(records)} new checklist!')
    time.sleep(2)
    
