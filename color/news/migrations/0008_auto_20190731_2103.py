# Generated by Django 2.1.7 on 2019-07-31 13:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20190731_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 31, 21, 3, 58, 35408), verbose_name='创建时间'),
        ),
    ]