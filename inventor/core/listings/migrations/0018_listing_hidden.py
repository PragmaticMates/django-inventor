# Generated by Django 2.2.4 on 2020-10-04 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0017_auto_20200708_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='hidden'),
        ),
    ]