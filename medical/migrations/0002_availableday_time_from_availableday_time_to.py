# Generated by Django 5.1.5 on 2025-01-30 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='availableday',
            name='time_from',
            field=models.TimeField(blank=True, default=datetime.time(15, 0)),
        ),
        migrations.AddField(
            model_name='availableday',
            name='time_to',
            field=models.TimeField(blank=True, default=datetime.time(21, 0)),
        ),
    ]
