# Generated by Django 5.1.4 on 2024-12-16 18:31

import base.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', base.models.CustomUserManager()),
            ],
        ),
    ]
