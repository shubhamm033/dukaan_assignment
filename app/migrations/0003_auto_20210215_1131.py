# Generated by Django 3.1.6 on 2021-02-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210215_0606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='update_at',
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
