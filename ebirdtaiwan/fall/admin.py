from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import SignupData, Survey, SurveyObs

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
    menu_label = '競賽清單'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    list_display = ('creator', 'scrape_date','checklist_id','latitude','longitude')
    list_filter = ('creator', 'scrape_date')
    # search_fields = ('team','ebirdid','ebirdid')

modeladmin_register(SurveyAdmin)


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