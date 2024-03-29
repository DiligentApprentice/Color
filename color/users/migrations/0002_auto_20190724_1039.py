# Generated by Django 2.1.7 on 2019-07-24 02:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '用户表'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='brief',
            field=models.TextField(blank=True, null=True, verbose_name='用户简介'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='所在城市'),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 24, 10, 39, 35, 204482), verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='github_link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='github链接'),
        ),
        migrations.AddField(
            model_name='user',
            name='link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='个人链接'),
        ),
        migrations.AddField(
            model_name='user',
            name='nick_name',
            field=models.CharField(blank=True, max_length=255, verbose_name=''),
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='头衔'),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='wb_link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='微博链接'),
        ),
        migrations.AddField(
            model_name='user',
            name='zh_link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='知乎链接'),
        ),
    ]
