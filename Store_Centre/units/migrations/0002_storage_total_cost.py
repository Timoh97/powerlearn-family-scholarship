# Generated by Django 4.1.7 on 2023-03-27 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='total_cost',
            field=models.IntegerField(default=0),
        ),
    ]
