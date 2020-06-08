# Generated by Django 2.2.4 on 2020-06-08 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_exercise_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='in_stock',
            field=models.SmallIntegerField(blank=True, default=None, help_text='empty value means infinite availability', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='in stock'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, default=None, help_text='EUR', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price'),
        ),
    ]
