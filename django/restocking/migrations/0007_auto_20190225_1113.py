# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-25 11:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restocking', '0006_orderitem_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, 'There is a value that is less than 0')]),
        ),
    ]