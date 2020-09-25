# Generated by Django 3.1 on 2020-09-25 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fall', '0014_auto_20200923_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutumnChanllengeData',
            fields=[
                ('checklist_id', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='清單ID')),
                ('scrape_date', models.DateField(auto_now_add=True, verbose_name='清單抓取日期')),
                ('survey_datetime', models.DateTimeField(auto_now_add=True, verbose_name='調查時間')),
                ('creator', models.CharField(editable=False, max_length=30, verbose_name='清單分享來源')),
                ('latitude', models.FloatField(default=23.5, verbose_name='緯度')),
                ('longitude', models.FloatField(default=120.5, verbose_name='經度')),
                ('county', models.CharField(default='天國市地獄鎮', max_length=15, verbose_name='鄉鎮名稱')),
                ('is_valid', models.BooleanField(editable=False, verbose_name='有鳥才算數')),
            ],
        ),
        migrations.AlterField(
            model_name='autumnchallengepage',
            name='dash_board_name',
            field=models.CharField(help_text="DON't TOUCH this", max_length=30),
        ),
    ]