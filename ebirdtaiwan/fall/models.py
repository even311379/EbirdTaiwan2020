from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from wagtailmenus.models import MenuPage
# Create your models here.

class Info(Page):

    info_content = RichTextField(blank=True, help_text='秋季觀鳥競賽的活動說明')

    content_panels = Page.content_panels + [
        FieldPanel('info_content', classname='full'),
    ]

class Reward(Page):

    reward_content = RichTextField(blank=True, help_text='秋季觀鳥競賽的獎品說明')

    content_panels = Page.content_panels + [
        FieldPanel('reward_content', classname='full')
    ]


class TeamIntroduction(Page):

    reward_content = RichTextField(blank=True, help_text='各隊伍介紹')

    content_panels = Page.content_panels + [
        FieldPanel('reward_content', classname='full')
    ]

class DashBoard(MenuPage):

    dash_board_name = models.CharField(max_length=30, blank=False, help_text="DON'tT TOUCH this")

    content_panels = Page.content_panels + [
        FieldPanel('dash_board_name', classname='full')
    ]