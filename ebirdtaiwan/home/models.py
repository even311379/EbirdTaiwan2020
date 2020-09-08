from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

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
    models.ImageField()
    content_panels = Page.content_panels + [
        FieldPanel('dash_grah_id'),
        ImageChooserPanel('team1_icon'),
        ImageChooserPanel('team2_icon'),
        ImageChooserPanel('team3_icon'),        
    ]


class PageFolder(Page):
    pass
