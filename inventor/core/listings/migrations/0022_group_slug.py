# Generated by Django 2.2.9 on 2021-03-20 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0021_auto_20210320_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]