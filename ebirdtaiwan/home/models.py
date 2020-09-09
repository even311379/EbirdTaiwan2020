from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
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

    content_panels = Page.content_panels + [
        FieldPanel('dash_grah_id'),
        MultiFieldPanel([
            FieldPanel('team1_name'),
            ImageChooserPanel('team1_icon'),
            FieldPanel('team2_name'),
            ImageChooserPanel('team2_icon'),
            FieldPanel('team3_name'),
            ImageChooserPanel('team3_icon'),        
        ], heading='Team',classname="collapsible"),
        MultiFieldPanel([
            ImageChooserPanel('corporation_icon1'),
            ImageChooserPanel('corporation_icon2')
        ], heading='Corporation',classname="collapsible")
    ]


class PageFolder(Page):
    pass
