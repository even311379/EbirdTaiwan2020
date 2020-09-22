import sys
import os
import django
from django.conf import settings
sys.path.append(os.path.abspath('ebirdtaiwan'))
import datetime
# sys.path.append(os.path.abspath(''))
# print(sys.path)
# from automaton import passwords

from ebirdtaiwan.settings.base import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from fall.models import Survey, SurveyObs

NewSurvey = Survey(
    scrape_date = datetime.date.today(),
    checklist_id='546788',
    team='test',
    creator='this is so good',
    survey_datetime=datetime.datetime.now(),
    latitude=23.225,
    longitude=121.332)
NewSurvey.save()

SurveyObs.objects.create(survey=Survey.objects.get(checklist_id='546788'), species_name='test_bird', amount=100)
# NewSurveyObs = SurveyObs(
#     survey = survey__id='546788',
#     species_name='test_bird',
#     amount = 100
# )
# NewSurveyObs.save()