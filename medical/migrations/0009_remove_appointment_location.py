# Generated by Django 5.1.5 on 2025-02-17 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0008_alter_appointment_appointment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='location',
        ),
    ]
