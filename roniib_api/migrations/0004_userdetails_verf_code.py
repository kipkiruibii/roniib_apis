# Generated by Django 4.2.5 on 2023-09-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roniib_api', '0003_userdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='verf_code',
            field=models.CharField(default='verfx', max_length=255),
        ),
    ]
