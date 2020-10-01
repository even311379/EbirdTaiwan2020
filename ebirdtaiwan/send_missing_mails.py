import datetime
import sys
import os
import django
from django.conf import settings
sys.path.append(os.path.abspath('ebirdtaiwan'))

from ebirdtaiwan.settings.base import DATABASES, INSTALLED_APPS, TEMPLATES
[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['.']
}]
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS, TEMPLATES=TEMPLATES)
django.setup()

from django.core.mail import EmailMessage
from django.template.loader import get_template

from fall.models import SignupData
import eb_passwords


def send_validation_email(email, team, ebirdid):
    t = get_template('fall/welcome_email_complex.html')
    content = t.render(locals())
    msg = EmailMessage(
        '歡迎加入ebirdTaiwan秋季挑戰賽',
        content,
        eb_passwords.mailserver_account,
        [email]
    )
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        print(e)


missing_mails = SignupData.objects.filter(signup_time__gte=datetime.datetime(2020,9,26))[5:21]
for i in missing_mails:
    send_validation_email(i.email, i.team, i.ebirdid)    

