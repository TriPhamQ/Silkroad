# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]