# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-01 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default=True, upload_to='post_images/'),
        ),
    ]
