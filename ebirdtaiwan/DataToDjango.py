import sys
import os
import django
from django.conf import settings
sys.path.append(os.path.abspath('ebirdtaiwan'))
# sys.path.append(os.path.abspath(''))
# print(sys.path)
# from automaton import passwords

from ebirdtaiwan.settings.base import DATABASES, INSTALLED_APPS
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from fall.models import Survey

NewSurvey = Survey(creator='this is so good', checklist_id='546788', latitude=23.225, longitude=121.332)
NewSurvey.save()
