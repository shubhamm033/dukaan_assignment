# Generated by Django 3.1.6 on 2021-02-15 12:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210215_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seller',
            name='password',
            field=models.CharField(default='password', max_length=255),
            preserve_default=False,
        ),
    ]
