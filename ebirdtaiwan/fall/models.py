from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from wagtailmenus.models import MenuPage

from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import get_template
from automation import passwords

# import datetime

class Info(Page):

    info_content = RichTextField(blank=True, help_text='秋季觀鳥競賽的活動說明')
    choose_team_page = models.ForeignKey( Page,null=True,blank=True, \
        on_delete=models.SET_NULL,related_name='+')
    prize_page = models.ForeignKey( Page,null=True,blank=True, \
        on_delete=models.SET_NULL,related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('info_content', classname='full'),
        FieldPanel('choose_team_page'),
        FieldPanel('prize_page'),
    ]

class Reward(Page):

    reward_content = RichTextField(blank=True, help_text='秋季觀鳥競賽的獎品說明')

    content_panels = Page.content_panels + [
        FieldPanel('reward_content', classname='full')
    ]


class TeamIntroduction(Page):

    team_left_description = models.CharField(blank=True, max_length=100, help_text='彩鷸隊')
    team_middle_description = models.CharField(blank=True, max_length=100, help_text='家燕隊')
    team_right_description = models.CharField(blank=True, max_length=100, help_text='大冠鷲隊')
    signup_page = models.ForeignKey( Page,null=True,blank=True, \
        on_delete=models.SET_NULL,related_name='+')
    content_panels = Page.content_panels + [
        FieldPanel('team_left_description'),
        FieldPanel('team_middle_description'),
        FieldPanel('team_right_description'),
        FieldPanel('signup_page')
    ]

class Dashboard(MenuPage):

    dash_board_name = models.CharField(max_length=30, blank=False, help_text="DON'tT TOUCH this")
    IsDemoApp = models.BooleanField(default=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('IsDemoApp'),
        FieldPanel('dash_board_name', classname='full')
    ]


class SignupData(models.Model):

    team_choice = [
        ('彩鷸隊', '彩鷸隊' ),
        ('家燕隊', '家燕隊' ),
        ('大冠鷲隊', '大冠鷲隊' ),
    ]

    ebirdid = models.CharField(max_length=50)
    team = models.CharField(max_length=6, choices=team_choice, default='彩鷸隊')
    email = models.EmailField(max_length=100)    
    signup_time = models.DateTimeField(auto_now_add=True, editable=False)  

    def __str__(self):
        return self.ebirdid

def send_validation_email(email, team, ebirdid):
    t = get_template('fall/welcome_email_complex.html')
    content = t.render(locals())
    msg = EmailMessage(
        '歡迎加入ebirdTaiwan秋季挑戰賽',
        content,
        passwords.mailserver_account,
        [email]
    )
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        print(e)


class SignupPage(Page):

    def serve(self, request):

        if request.method == 'POST':            
            ebirdid = request.POST.get('ebirdid', None)
            team = request.POST.get('team', None)            
            email = request.POST.get('email', None)            
            if (len(SignupData.objects.filter(ebirdid=ebirdid)) > 0):
                return render(request, 'fall/signup.html', {'page': self, 'error_message': '這個eBird公開顯示名稱已經註冊了！'})
            if (len(SignupData.objects.filter(email=email)) > 0):
                return render(request, 'fall/signup.html', {'page': self, 'error_message': '這個email註冊過了！'})

            send_validation_email(email = email, team = team, ebirdid = ebirdid)
            '''
            TODO: add email valid check before add data
            '''
            NewSignupData = SignupData(
                ebirdid=ebirdid,
                team = team,
                email=email,                
            )            
            NewSignupData.save()
            
            return render(request, 'fall/thankyou.html', {'page': self, 'ebirdid':ebirdid, 'team':team})
        else:
            print('it is get...')
            return render(request, 'fall/signup.html', {'page': self, 'error_message':'' })


class PredictionData(models.Model):
    
    participant_name = models.CharField(blank=False, max_length=40)
    participant_email = models.EmailField(max_length=100)
    guess_n_species = models.IntegerField(default=0)
    guess_total_individual = models.IntegerField(default=0)
    prediction_datetime = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.participant_name + self.participant_email


class SubmitPrediction(Page):


    def serve(self, request):
        if request.method == 'POST':
            name = request.POST.get('participant_name', None)
            print('????')
            print(name)
            email = request.POST.get('participant_email', None)            
            gns = request.POST.get('guess_n_species', None)
            gni = request.POST.get('guess_total_individual', None)  
            
            if (len(PredictionData.objects.filter(participant_email=email)) > 0):
                return render(request, 'fall/prediction.html', {'page': self, 'error_message': '錯誤！一個email只能進行一次預測'})

            NewPredictionData = PredictionData(
                participant_name = name,
                participant_email = email,
                guess_n_species = gns,
                guess_total_individual = gni
            )

            NewPredictionData.save()

            return render(request, 'fall/prediction_finish.html', {'page': self})
        else:
            return render(request, 'fall/prediction.html', {'page': self, 'error_message': ''})

        


'''
Scraped data area
'''

class Survey(models.Model):
    scrape_date = models.DateField(editable=False,auto_now_add=True)
    team = models.CharField(blank=False, max_length=5, default='沒有隊')
    checklist_id = models.CharField(blank=False, max_length=15, primary_key=True)
    creator = models.CharField(blank=False, max_length=30)
    survey_datetime = models.DateTimeField(blank=False, verbose_name='調查時間', null=True) #try out will set verbose name good?
    latitude = models.FloatField(blank=False, default=23.5)
    longitude = models.FloatField(blank=False, default=120.5)

    def __str__(self):
        return self.checklist_id


class SurveyObs(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    species_code = models.CharField(blank=False, max_length=10, default='aalife')
    species_tranlated_name = models.CharField(blank=False, max_length=30, default='unKnown')
    amount = models.IntegerField(blank=False, default=0)





