# Generated by Django 3.1 on 2020-09-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fall', '0015_auto_20200925_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autumnchanllengedata',
            name='survey_datetime',
            field=models.DateTimeField(editable=False, verbose_name='調查時間'),
        ),
    ]
