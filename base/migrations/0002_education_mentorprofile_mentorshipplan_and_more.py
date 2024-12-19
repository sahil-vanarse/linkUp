# Generated by Django 5.1.4 on 2024-12-19 13:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=200)),
                ('degree', models.CharField(choices=[('HS', 'High School'), ('BA', "Bachelor's"), ('MA', "Master's"), ('PHD', 'Doctorate'), ('OTH', 'Other')], max_length=3)),
                ('field_of_study', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Education',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('verification_status', models.CharField(choices=[('P', 'Pending'), ('V', 'Verified'), ('R', 'Rejected')], default='P', max_length=1)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('about', models.TextField()),
                ('years_of_experience', models.PositiveIntegerField()),
                ('expertise_areas', models.ManyToManyField(related_name='mentor_expertise', to='base.topic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration_months', models.PositiveIntegerField(choices=[(1, '1 Month'), (2, '2 Months'), (3, '3 Months'), (6, '6 Months')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('meetings_per_month', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('is_active', models.BooleanField(default=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentorship_plans', to='base.mentorprofile')),
            ],
            options={
                'unique_together': {('mentor', 'duration_months')},
            },
        ),
        migrations.CreateModel(
            name='MentorshipEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Active'), ('C', 'Completed'), ('CA', 'Cancelled')], default='P', max_length=2)),
                ('payment_id', models.CharField(max_length=100, unique=True)),
                ('payment_status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentee_enrollments', to=settings.AUTH_USER_MODEL)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.mentorshipplan')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_experiences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
    ]
