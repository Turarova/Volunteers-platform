# Generated by Django 5.1.2 on 2025-02-24 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0005_alter_user_email_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='volunteer.company'),
        ),
    ]
