# Generated by Django 5.1.5 on 2025-02-06 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='reset_code_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
