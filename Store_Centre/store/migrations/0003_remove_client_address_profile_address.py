# Generated by Django 4.1.7 on 2023-03-29 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_client_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='address',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
