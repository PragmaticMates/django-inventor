# Generated by Django 2.2.4 on 2020-06-08 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20200608_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='awaiting',
            field=models.BooleanField(default=False, verbose_name='awaiting'),
        ),
    ]
