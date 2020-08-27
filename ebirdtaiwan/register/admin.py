from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import JoinData

class JoinDataAdmin(ModelAdmin):
    model = JoinData
    menu_label = '報名資料'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    list_display = ('ebirdid', 'email','password','team','register_time','is_valid')
    list_filter = ('team', 'register_time')
    search_fields = ('team', 'register_time',)



modeladmin_register(JoinDataAdmin)