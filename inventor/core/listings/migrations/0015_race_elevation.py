# Generated by Django 2.2.4 on 2020-07-03 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0014_auto_20200702_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='elevation',
            field=models.PositiveSmallIntegerField(blank=True, default=None, help_text='m', null=True, verbose_name='elevation'),
        ),
    ]
