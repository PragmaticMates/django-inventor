# Generated by Django 2.2.4 on 2020-03-09 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='booking_url',
            field=models.URLField(blank=True, max_length=300, verbose_name='booking URL'),
        ),
        migrations.AddField(
            model_name='eatanddrink',
            name='booking_url',
            field=models.URLField(blank=True, max_length=300, verbose_name='booking URL'),
        ),
    ]
