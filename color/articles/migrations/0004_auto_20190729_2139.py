# Generated by Django 2.1.7 on 2019-07-29 13:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20190729_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2019, 7, 29, 21, 39, 51, 669224), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='slug',
            field=models.SlugField(blank=True, max_length=80, null=True, verbose_name='转化文章详情页URL'),
        ),
    ]
