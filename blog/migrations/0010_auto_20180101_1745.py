# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-01 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20180101_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='post_images/'),
        ),
    ]