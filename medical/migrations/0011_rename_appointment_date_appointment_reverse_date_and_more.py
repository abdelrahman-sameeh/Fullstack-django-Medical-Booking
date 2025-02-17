# Generated by Django 5.1.5 on 2025-02-17 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0010_alter_appointment_appointment_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='appointment_date',
            new_name='reverse_date',
        ),
        migrations.AddField(
            model_name='appointment',
            name='predict_time_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='predict_time_start',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
