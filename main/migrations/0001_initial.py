# Generated by Django 5.1.2 on 2024-11-13 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Needy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('about_me', models.TextField(help_text='Өзүңүз жөнүндө кыскача маалымат бериңиз')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True)),
                ('help_description', models.TextField()),
            ],
        ),
    ]
