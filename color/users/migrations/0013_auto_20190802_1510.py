# Generated by Django 2.1.7 on 2019-08-02 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190731_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 15, 10, 54, 912669), verbose_name='创建时间'),
        ),
    ]
