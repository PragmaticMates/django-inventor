# Generated by Django 2.2.4 on 2020-07-02 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0013_listing_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='options',
            field=models.ManyToManyField(blank=True, to='commerce.Option', verbose_name='options'),
        ),
    ]