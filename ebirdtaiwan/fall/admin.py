from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import SignupData

# add to wagtail admin
class SignupDataAdmin(ModelAdmin):
    model = SignupData
    menu_label = '報名資料'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    list_display = ('team', 'ebirdid','email','signup_time')
    list_filter = ('team', 'signup_time')
    search_fields = ('team','ebirdid','ebirdid')

modeladmin_register(SignupDataAdmin)


# add to django admin
class SignupDataDAdmin(admin.ModelAdmin):
    list_display = ('team', 'ebirdid','email','signup_time')
    list_filter = ('team', 'signup_time')
    
admin.site.register(SignupData, SignupDataDAdmin)
