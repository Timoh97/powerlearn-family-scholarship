# Generated by Django 4.1.7 on 2023-03-27 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0006_goods_no_of_units'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='no_of_units',
            new_name='available_units',
        ),
    ]
