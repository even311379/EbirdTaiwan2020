# Generated by Django 3.1 on 2020-09-23 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fall', '0012_auto_20200922_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='brython_file_name',
            field=models.CharField(blank=True, help_text='page_instance_specific brython script', max_length=30),
        ),
    ]
