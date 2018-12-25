# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-25 14:13
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImagesMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='文件名')),
                ('fds_path', models.ImageField(blank=True, upload_to='', verbose_name='上传图片地址')),
                ('upload_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='上传时间')),
                ('space', models.CharField(blank=True, max_length=100, null=True, verbose_name='空间名')),
                ('file_desc', DjangoUeditor.models.UEditorField(blank=True, default='', null=True, verbose_name='内容')),
            ],
            options={
                'verbose_name': '上传信息',
                'verbose_name_plural': '上传信息',
                'db_table': 'upload_images_message',
            },
        ),
    ]
