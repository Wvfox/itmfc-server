# Generated by Django 5.1.1 on 2024-12-24 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0007_application_layout_application_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='owner_tg',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Owner tg'),
        ),
    ]
