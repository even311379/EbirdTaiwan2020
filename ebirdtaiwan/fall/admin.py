from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import SignupData, Survey, SurveyObs, PredictionData

# add to wagtail admin
class SignupDataAdmin(ModelAdmin):
    model = SignupData
    menu_label = '報名資料'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    list_display = ('team', 'ebirdid','email','signup_time')
    list_filter = ('team', 'signup_time')
    search_fields = ('team','ebirdid','ebirdid')

modeladmin_register(SignupDataAdmin)

class SurveyAdmin(ModelAdmin):
    model = Survey
    menu_label = '競賽上傳清單'  # ditch this to use verbose_name_plural from model
    menu_icon = 'doc-empty'  # change as required
    list_display = ('creator', 'scrape_date','checklist_id','latitude','longitude')
    list_filter = ('creator', 'scrape_date')
    # search_fields = ('team','ebirdid','ebirdid')

modeladmin_register(SurveyAdmin)

class PredictionDataAdmin(ModelAdmin):
    model = PredictionData
    menu_label = '民眾預測'
    menu_icon = 'success'
    list_display = ('participant_name', 'participant_email','guess_n_species','guess_total_individual','prediction_datetime')
    search_fields = ('participant_name',)

modeladmin_register(PredictionDataAdmin)

# add to django admin
class SignupDataDAdmin(admin.ModelAdmin):
    list_display = ('team', 'ebirdid','email','signup_time')
    list_filter = ('team', 'signup_time')
    
admin.site.register(SignupData, SignupDataDAdmin)


class SurveyDAdmin(admin.ModelAdmin):
    list_display = ('creator', 'scrape_date','checklist_id','latitude','longitude')
    list_filter = ('creator', 'scrape_date')
    # search_fields = ('team','ebirdid','ebirdid')

admin.site.register(Survey, SurveyDAdmin)