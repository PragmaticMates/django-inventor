# Generated by Django 2.2.14 on 2021-12-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0023_auto_20210523_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='rank',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='rank'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='availability',
            field=models.CharField(choices=[('STOCK', 'stock'), ('INFINITE', 'infinite'), ('DIGITAL_GOODS', 'digital goods'), ('SALE_ENDED', 'sale ended')], default='STOCK', max_length=13, verbose_name='availability'),
        ),
    ]
