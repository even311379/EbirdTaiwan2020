from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField

from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import get_template

import random
from automation import passwords


class JoinData(models.Model):

    team_choice = [
        ('大冠隊', '大冠隊' ),
        ('彩鷸隊', '彩鷸隊' ),
        ('家雁隊', '家雁隊' ),
    ]

    ebirdid = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
    team = models.CharField(max_length=3, choices=team_choice, default='大冠隊')
    register_time = models.DateTimeField(auto_now=False, auto_now_add=True)    
    is_valid = models.BooleanField(default=False)
    validation_code = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.name



def RandomValidationCode():
    c = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    s = ''
    for i in range(20):
        s+=random.choice(c)
    return s


def send_validation_email(email, validation_url, ebirdID):
    t = get_template('register/validation_email.html')
    content = t.render(locals())
    msg = EmailMessage(
        '認證ebirdTaiwn 秋季挑戰賽帳號',
        content,
        passwords.mailserver_account,
        [email]
    )
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        print(e)



'''
The form builder is so fucking ugly...
just use my own way...
'''
class RegisterPage(Page):

    intro = RichTextField(blank=True)
    validaing = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('validaing', classname="full"),
        FieldPanel('thank_you_text', classname="full"),        
    ]


    def serve(self, request):
        
        if request.method == 'POST':            
            print('Its a post, I can do more things')
            ebirdid = request.POST.get('ebirdid', None)
            email = request.POST.get('email', None)
            password = request.POST.get('password', None)
            team = request.POST.get('team', None)            
            validation_code = RandomValidationCode()
            NewJoinData = JoinData(
                ebirdid=ebirdid,
                email=email,
                password = password,
                team = team,
                validation_code = validation_code,
            )            
            NewJoinData.save()
            vu = 'https://' + request.get_host()+self.url+'?validation_code='+validation_code
            send_validation_email(email = email, validation_url = vu, ebirdID = ebirdid)
            '''
            save files to data base
            '''
            return render(request, 'register/validation.html', {'page': self})
        else:            
            validation_code = request.GET.get('validation_code', None)            
            if validation_code:
                unvalid_data = JoinData.objects.filter(validation_code__exact=validation_code)
                validation_pass = False
                if unvalid_data:
                    unvalid_data[0].is_valid = True
                    # print(dir(unvalid_data))
                    unvalid_data[0].save()
                    validation_pass = True                
                
                return render(request, 'register/thank_you.html', {'page': self, 'validation_pass': validation_pass})
            print(request.get_host())
            print(self.url)
            return render(request, 'register/register_form.html', {'page': self})








