# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-05 09:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20180202_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default=b'img/categories/cake.png', null=True, upload_to=b'img/categories/'),
        ),
        migrations.AlterField(
            model_name='group',
            name='category_ref',
            field=models.ForeignKey(help_text=b'Specify the category', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Category', verbose_name=b'Category'),
        ),
    ]
