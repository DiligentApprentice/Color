# Generated by Django 2.1.7 on 2019-07-29 06:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20190729_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 29, 14, 17, 5, 816004), verbose_name='创建时间'),
        ),
    ]
