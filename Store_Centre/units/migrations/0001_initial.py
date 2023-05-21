# Generated by Django 4.2 on 2023-05-02 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=100)),
                ('charge', models.IntegerField()),
                ('no_unit', models.IntegerField(blank=True, default=0)),
                ('available_unit', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_unit', models.IntegerField(blank=True, null=True)),
                ('arrival_date', models.DateField()),
                ('departure_date', models.DateField()),
                ('description', models.TextField(max_length=500)),
                ('total_cost', models.IntegerField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to=settings.AUTH_USER_MODEL)),
                ('storage_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='units', to='units.storage')),
            ],
        ),
    ]
