# Generated by Django 2.1.7 on 2019-07-31 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20190730_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 31, 20, 53, 3, 496709), verbose_name='创建时间'),
        ),
    ]
