# Generated by Django 2.2.4 on 2020-07-06 17:24

import django.contrib.postgres.indexes
from django.db import migrations, models
import modeltrans.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0015_race_elevation'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='description',
            field=models.CharField(blank=True, max_length=50, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='photo',
            name='i18n',
            field=modeltrans.fields.TranslationField(fields=('description',), required_languages=(), virtual_fields=True),
        ),
        migrations.AddIndex(
            model_name='photo',
            index=django.contrib.postgres.indexes.GinIndex(fields=['i18n'], name='listings_ph_i18n_27b296_gin'),
        ),
    ]