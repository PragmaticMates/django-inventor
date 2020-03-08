# Generated by Django 2.2.4 on 2020-03-08 13:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_listing_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='rooms',
            field=models.SmallIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='number of rooms'),
        ),
    ]
