# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-25 20:49
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FdsMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_ip', models.GenericIPAddressField(verbose_name='客户端上传ip')),
                ('fds_storage_path', models.FilePathField(max_length=200, path='/group1/M00', verbose_name='fds存储位置')),
                ('group_name', models.CharField(max_length=100, verbose_name='上传群主')),
                ('fds_add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='fds添加时间')),
                ('upload_status', models.CharField(max_length=100, verbose_name='上传fds状态')),
                ('fds_size', models.FloatField(default=0, verbose_name='fds文件大小')),
            ],
            options={
                'verbose_name': '文件信息',
                'verbose_name_plural': '文件信息',
            },
        ),
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100, verbose_name='文件名')),
                ('filesize', models.IntegerField(default=0, verbose_name='文件大小')),
                ('stype', models.CharField(max_length=100, verbose_name='文件类型')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='文件创建时间')),
                ('local_storage_path', models.FilePathField(max_length=200, path='/media/file', verbose_name='本地存储位置')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否已删除')),
                ('space', models.CharField(max_length=100, verbose_name='空间名')),
                ('file_desc', DjangoUeditor.models.UEditorField(default='', verbose_name='内容')),
            ],
            options={
                'verbose_name': '文件信息',
                'verbose_name_plural': '文件信息',
            },
        ),
        migrations.CreateModel(
            name='UploadMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('remark', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '上传信息',
                'verbose_name_plural': '上传信息',
            },
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='md5_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_files.UploadMessage', verbose_name='md5值'),
        ),
    ]
