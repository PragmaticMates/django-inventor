# Generated by Django 2.2.4 on 2020-06-23 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='distance',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, help_text='km', max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='distance'),
        ),
    ]
