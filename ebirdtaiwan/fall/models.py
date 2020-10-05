from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from wagtailmenus.models import MenuPage

from django.shortcuts import render
from django.core.mail import EmailMessage
from django.template.loader import get_template

import pandas as pd
import datetime
import eb_passwords

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
    brython_file_name = models.CharField(max_length=30, blank=True, help_text='page_instance_specific brython script')

    content_panels = Page.content_panels + [
        FieldPanel('IsDemoApp'),
        FieldPanel('dash_board_name', classname='full'),
        FieldPanel('brython_file_name')
    ]


class SignupData(models.Model):

    team_choice = [
        ('彩鷸隊', '彩鷸隊' ),
        ('家燕隊', '家燕隊' ),
        ('大冠鷲隊', '大冠鷲隊' ),
    ]

    ebirdid = models.CharField(max_length=50, verbose_name='ebird公開帳號')
    team = models.CharField(max_length=6, choices=team_choice, default='彩鷸隊', verbose_name='隊伍名稱')
    email = models.EmailField(max_length=100, verbose_name='電子信箱')    
    signup_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='報名時間')  

    def __str__(self):
        return self.ebirdid

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


class SignupPage(Page):

    def serve(self, request):

        if request.method == 'POST':            
            ebirdid = request.POST.get('ebirdid', None)
            team = request.POST.get('team', None)            
            email = request.POST.get('email', None)            
            if (len(SignupData.objects.filter(ebirdid=ebirdid)) > 0):
                render_data = locals()
                render_data['page'] = self
                render_data['error_message'] = '這個eBird公開顯示名稱已經註冊了！'
                return render(request, 'fall/signup.html', render_data)
            if (len(SignupData.objects.filter(email=email)) > 0):
                render_data = locals()
                render_data['page'] = self
                render_data['error_message'] = '這個email註冊過了！'
                return render(request, 'fall/signup.html', render_data)

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
            render_data = locals()
            render_data['page'] = self
            return render(request, 'fall/thankyou.html', render_data)
        else:
            render_data = locals()
            render_data['page'] = self
            return render(request, 'fall/signup.html', render_data)


class AutumnChallengePage(Page):

    subtitle = RichTextField(blank=True)
    rules = RichTextField(blank=True)
    prizes = RichTextField(blank=True)
    dash_board_name = models.CharField(max_length=30, blank=False, help_text="DON't TOUCH this")    

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('rules', classname='full'),
        FieldPanel('prizes', classname='full'),
        FieldPanel('dash_board_name')
    ]

    def serve(self, request):

        recent_data20 = AutumnChanllengeData.objects.all().order_by('-survey_datetime')[:20]
        df = pd.DataFrame.from_records(recent_data20.values('creator','county','survey_datetime'))[::-1]
        if len(df) > 0:
            peoples = df['creator'].tolist()
            towns = df['county'].tolist()
            upload_time = [datetime.datetime.strftime(t, '%Y-%m-%d %H:%M:%S') for t in df['survey_datetime'].tolist()]
        else:
            peoples = []
            towns = []
            upload_time = []
        render_data = locals()
        render_data['page'] = self
        return render(request, 'fall/autumn_challenge_page.html', render_data)


class PredictionData(models.Model):
    
    participant_name = models.CharField(blank=False, max_length=40, verbose_name='參與者名稱')   
    participant_phone = models.CharField(max_length=30, verbose_name='聯絡電話',default='0912345678')
    guess_n_species = models.IntegerField(default=0, verbose_name='幾種物種？')
    guess_total_individual = models.IntegerField(default=0, verbose_name='全部幾隻？')
    prediction_datetime = models.DateTimeField(auto_now=True, editable=False, verbose_name='何時進行預測')

    def __str__(self):
        return self.participant_name + self.participant_phone


class SubmitPrediction(Page):


    def serve(self, request):
        if request.method == 'POST':
            name = request.POST.get('participant_name', None)
            phone = request.POST.get('participant_phone', None)            
            gns = request.POST.get('guess_n_species', None)
            gni = request.POST.get('guess_total_individual', None)  
            
            if (len(PredictionData.objects.filter(participant_phone=phone)) > 0):
                render_data = locals()
                render_data['page'] = self
                render_data['error_message'] =  '錯誤！一組電話只能進行一次預測'
                return render(request, 'fall/prediction.html', render_data)

            NewPredictionData = PredictionData(
                participant_name = name,
                participant_phone = phone,
                guess_n_species = gns,
                guess_total_individual = gni
            )

            NewPredictionData.save()
            render_data = locals()
            render_data['page'] = self
            return render(request, 'fall/prediction_finish.html', render_data)
        else:
            render_data = locals()
            render_data['page'] = self
            return render(request, 'fall/prediction.html', render_data)

        


'''
Scraped data area
'''

class Survey(models.Model):
    scrape_date = models.DateField(editable=False,auto_now_add=True,verbose_name='清單抓取日期')
    team = models.CharField(blank=False, max_length=5, default='沒有隊',verbose_name='隊伍名稱')
    checklist_id = models.CharField(blank=False, max_length=15, primary_key=True,verbose_name='清單ID')
    creator = models.CharField(blank=False, max_length=30,verbose_name='清單分享來源')
    survey_datetime = models.DateTimeField(blank=False, verbose_name='調查時間', null=True) #try out will set verbose name good?
    latitude = models.FloatField(blank=False, default=23.5,verbose_name='緯度')
    longitude = models.FloatField(blank=False, default=120.5,verbose_name='經度')
    county = models.CharField(default='天國市地獄鎮',max_length=15,verbose_name='鄉鎮名稱')    
    is_valid = models.BooleanField(default=False,verbose_name='是否完整') #checklist不含X 大於5分鐘    

    def __str__(self):
        return self.checklist_id


class SurveyObs(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='清單ID')    
    species_name = models.CharField(blank=False, max_length=30, default='unKnown', verbose_name='物種名稱')
    amount = models.IntegerField(blank=False, default=0, verbose_name='數量')

class AutumnChanllengeData(models.Model):
    checklist_id = models.CharField(blank=False, max_length=15, primary_key=True,verbose_name='清單ID')
    scrape_date = models.DateField(editable=False,auto_now_add=True,verbose_name='清單抓取日期')
    survey_datetime = models.DateTimeField(editable=False,auto_now_add=False,verbose_name='調查時間')
    creator = models.CharField(editable=False,blank=False, max_length=30,verbose_name='清單分享來源')
    latitude = models.FloatField(default=23.5,verbose_name='緯度')
    longitude = models.FloatField(default=120.5,verbose_name='經度')
    county = models.CharField(default='天國市地獄鎮',max_length=15,verbose_name='鄉鎮名稱')
    is_valid = models.BooleanField(editable=True,verbose_name='有鳥才算數')




