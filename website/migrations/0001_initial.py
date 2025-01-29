# Generated by Django 5.1.1 on 2025-01-29 15:49

import config.utilities
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(storage=config.utilities.UUIDFileStorage(), upload_to='vacancy')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date of creation')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
