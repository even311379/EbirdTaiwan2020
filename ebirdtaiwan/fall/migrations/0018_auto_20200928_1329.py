# Generated by Django 3.1 on 2020-09-28 05:29

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fall', '0017_auto_20200928_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autumnchallengepage',
            name='subtitle',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]