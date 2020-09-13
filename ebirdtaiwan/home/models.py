from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel

class AppDemoPage(Page):
    Title = models.CharField(blank=False ,max_length=255)
    body = StreamField([
        ('heading', blocks.CharBlock(True)),
        ('paragraph', blocks.RichTextBlock()),
        ('dash_graph_id', blocks.CharBlock(True)),

    ])

    content_panels = Page.content_panels + [
        FieldPanel('Title'),
        StreamFieldPanel('body'),
    ]

class HomePage(Page):

    dash_grah_id = models.CharField(blank=False ,max_length=255, help_text="Don't touch this value, the page may crash!!")

    team1_color = ColorField(default="#ffffff", help_text='the color for 彩鷸隊')
    team2_color = ColorField(default="#ffffff", help_text='the color for 家燕隊')
    team3_color = ColorField(default="#ffffff", help_text='the color for 大冠鷲隊')        

    content_panels = Page.content_panels + [
        FieldPanel('dash_grah_id'),
        NativeColorPanel('team1_color'),
        NativeColorPanel('team2_color'),
        NativeColorPanel('team3_color'),
    ]     

class PageFolder(Page):
    pass
