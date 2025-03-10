# Generated by Django 5.1.2 on 2025-02-24 10:22

import volunteer.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0009_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default=volunteer.models.generate_temp_email, error_messages={'unique': 'A user with this email address already exists.'}, help_text='Enter an email address in format: email@domain.com.', max_length=254, null=True, unique=True, verbose_name='Email'),
        ),
    ]
