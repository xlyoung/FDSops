# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-02 10:26
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media_files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmessage',
            name='file_desc',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', null=True, verbose_name='内容'),
        ),
    ]
