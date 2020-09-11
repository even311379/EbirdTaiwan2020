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

    dash_grah_id = models.CharField(blank=False ,max_length=255)

    title_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    team1_name = models.CharField(blank=True, max_length=10)
    team2_name = models.CharField(blank=True, max_length=10)
    team3_name = models.CharField(blank=True, max_length=10)

    team1_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    team2_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    team3_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    team1_color = ColorField(default="#ffffff")
    team2_color = ColorField(default="#ffffff")
    team3_color = ColorField(default="#ffffff")

    team1_welcome_title = models.CharField(blank=True, max_length=20)
    team2_welcome_title = models.CharField(blank=True, max_length=20)
    team3_welcome_title = models.CharField(blank=True, max_length=20)

    team1_welcome_content = RichTextField(blank=True)
    team2_welcome_content = RichTextField(blank=True)
    team3_welcome_content = RichTextField(blank=True)    

    corporation_icon1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    corporation_icon2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    register_url = models.CharField(blank=True, max_length=20)

    content_panels = Page.content_panels + [
        FieldPanel('dash_grah_id'),
        MultiFieldPanel([
            FieldPanel('team1_name',classname='title'),
            NativeColorPanel('team1_color'),
            ImageChooserPanel('team1_icon'),
            FieldPanel('team1_welcome_title'),
            FieldPanel('team1_welcome_content', classname='full'),                
        ], heading='Team1',classname="collapsible"),        
        MultiFieldPanel([
            FieldPanel('team2_name',classname='title'),
            NativeColorPanel('team2_color'),
            ImageChooserPanel('team2_icon'),
            FieldPanel('team2_welcome_title'),
            FieldPanel('team2_welcome_content', classname='full'),                
        ], heading='Team2',classname="collapsible"),        
        MultiFieldPanel([
            FieldPanel('team3_name',classname='title'),
            NativeColorPanel('team3_color'),
            ImageChooserPanel('team3_icon'),
            FieldPanel('team3_welcome_title'),
            FieldPanel('team3_welcome_content', classname='full'),                
        ], heading='Team3',classname="collapsible"),        
        MultiFieldPanel([
            ImageChooserPanel('title_icon'),
            ImageChooserPanel('corporation_icon1'),
            ImageChooserPanel('corporation_icon2')
        ],heading='PageIcons',classname='collapsible'),
        FieldPanel('register_url'),
    ]


class PageFolder(Page):
    pass
