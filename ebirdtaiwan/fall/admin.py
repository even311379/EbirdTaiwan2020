from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import SignupData, Survey, SurveyObs, PredictionData, AutumnChanllengeData

from .wagtail_hooks import ExportModelAdminMixin

####################################################
##############  wagtail admin     ###################
####################################################

class SignupDataAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "fall/export_csv.html"
    model = SignupData
    menu_label = '報名資料'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    list_display = ('team', 'ebirdid','email','signup_time')
    list_filter = ('team', 'signup_time')
    search_fields = ['ebirdid']

modeladmin_register(SignupDataAdmin)

class SurveyAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "fall/export_csv.html"
    model = Survey
    menu_label = '競賽上傳清單'
    menu_icon = 'doc-empty' 
    list_display = ('checklist_id','creator', 'team','scrape_date','survey_datetime','region_code','is_valid')
    list_filter = ('team','region_code', 'is_valid')
    search_fields = ['creator']


modeladmin_register(SurveyAdmin)


class SurveyObsAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "fall/export_csv.html"
    model = SurveyObs
    menu_label = '競賽上傳物種資料'
    menu_icon = 'doc-empty' 
    list_display = ('survey','species_name', 'amount')
    '''
    can use foreign key ex: survey__checklist_id...
    so good... so cool...
    '''    
    list_filter = ('survey__team', 'survey__creator')         
    search_fields = ['survey__checklist_id', 'species_name']

modeladmin_register(SurveyObsAdmin)

class PredictionDataAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "fall/export_csv.html"
    model = PredictionData
    menu_label = '民眾預測'
    menu_icon = 'success'
    list_display = ('participant_name', 'participant_email','guess_n_species','guess_total_individual','prediction_datetime')
    search_fields = ['participant_name',]

modeladmin_register(PredictionDataAdmin)


class ACDataAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "fall/export_csv.html"
    model = AutumnChanllengeData
    menu_label = '秋季挑戰賽資料'
    menu_icon = 'doc-empty'
    list_display = ('checklist_id', 'scrape_date','survey_datetime','creator','latitude','longitude','county','is_valid')
    list_filter = ('survey_datetime', 'county')
    search_fields = ['checklist_id', 'creator',]

modeladmin_register(ACDataAdmin)
####################################################
##############  django admin     ###################
####################################################
class SignupDataDAdmin(admin.ModelAdmin):
    list_display = ('team', 'ebirdid','email','signup_time')
    list_filter = ('team', 'signup_time')
    
admin.site.register(SignupData, SignupDataDAdmin)

class SurveyDAdmin(admin.ModelAdmin):
    list_display = ('checklist_id','creator', 'team','scrape_date','survey_datetime','region_code','is_valid')
    list_filter = ('team','region_code', 'is_valid')

admin.site.register(Survey, SurveyDAdmin)

class SurveyObsDAdmin(admin.ModelAdmin):
    list_display = ('survey','species_name', 'amount')    

admin.site.register(SurveyObs, SurveyObsDAdmin)

class PredictionDataDAdmin(admin.ModelAdmin):
    list_display = ('participant_name', 'participant_email','guess_n_species','guess_total_individual','prediction_datetime')
    search_fields = ['participant_name',]

admin.site.register(PredictionData, PredictionDataDAdmin)


class ACDataDAdmin(admin.ModelAdmin):
    list_display = ('checklist_id', 'scrape_date','survey_datetime','creator','latitude','longitude','county','is_valid')
    list_filter = ('survey_datetime', 'county')
    search_fields = ['checklist_id', 'creator',]

admin.site.register(AutumnChanllengeData, ACDataDAdmin)

