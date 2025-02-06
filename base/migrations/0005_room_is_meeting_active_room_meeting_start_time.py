# Generated by Django 5.1.4 on 2025-02-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_message_reply_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_meeting_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='meeting_start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
