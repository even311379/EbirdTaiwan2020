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

class upper_home(Page):

    event1_thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    event1_title = models.CharField(max_length=30, blank=False, help_text='秋季大亂鬥')
    event1_description = RichTextField()
    event1_period = models.CharField(max_length=20, blank=False)
    event1_page = models.ForeignKey( Page,null=True,blank=True, \
        on_delete=models.SET_NULL,related_name='+')


    event2_thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    event2_title = models.CharField(max_length=30, blank=False, help_text='全球觀鳥大日')
    event2_description = RichTextField()
    event2_period = models.CharField(max_length=20, blank=False)
    event2_url = models.CharField(max_length=40, blank=False, help_text='10/17全球官鳥大日的網址') 

    event3_thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    event3_title = models.CharField(max_length=30, blank=False, help_text='台北觀鳥大賽')
    event3_description = RichTextField()
    event3_period = models.CharField(max_length=20, blank=False)
    event3_page = models.ForeignKey( Page,null=True,blank=True, \
        on_delete=models.SET_NULL,related_name='+')


    content_panels = Page.content_panels + [

        MultiFieldPanel([
            ImageChooserPanel('event1_thumbnail'),
            FieldPanel('event1_title'),
            FieldPanel('event1_description'),
            FieldPanel('event1_period'),
            FieldPanel('event1_page')     
        ], heading='Event1',classname="collapsible"),
        MultiFieldPanel([
            ImageChooserPanel('event2_thumbnail'),
            FieldPanel('event2_title'),
            FieldPanel('event2_description'),
            FieldPanel('event2_period'),
            FieldPanel('event2_url')     
        ], heading='Event2',classname="collapsible"),
        MultiFieldPanel([
            ImageChooserPanel('event3_thumbnail'),
            FieldPanel('event3_title'),
            FieldPanel('event3_description'),
            FieldPanel('event3_period'),
            FieldPanel('event3_page')     
        ], heading='Event3',classname="collapsible"),
    ]