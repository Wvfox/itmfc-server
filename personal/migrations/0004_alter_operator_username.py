# Generated by Django 5.1.1 on 2024-12-18 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0003_alter_operator_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='username',
            field=models.SlugField(blank=True, max_length=64, null=True, unique=True, verbose_name='Username'),
        ),
    ]