# Generated by Django 5.1.1 on 2025-01-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0002_clip_is_submit'),
    ]

    operations = [
        migrations.AddField(
            model_name='clip',
            name='is_wrong',
            field=models.BooleanField(default=False),
        ),
    ]
