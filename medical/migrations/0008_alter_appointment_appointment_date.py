# Generated by Django 5.1.5 on 2025-02-17 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0007_remove_appointment_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
