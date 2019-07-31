# Generated by Django 2.1.7 on 2019-07-29 06:17

import datetime
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2019, 7, 29, 14, 17, 5, 849940), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='文章标签'),
        ),
    ]
