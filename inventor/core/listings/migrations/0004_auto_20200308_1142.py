# Generated by Django 2.2.4 on 2020-03-08 10:42

import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_remove_accommodation_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='social_networks',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict, verbose_name='social networks'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title'),
        ),
    ]
