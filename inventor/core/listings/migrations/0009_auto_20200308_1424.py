# Generated by Django 2.2.4 on 2020-03-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_auto_20200308_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='booking_period',
            field=models.CharField(blank=True, choices=[('HOUR', 'hour'), ('DAY', 'day'), ('NIGHT', 'night')], max_length=5, verbose_name='booking period'),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='bookings_max_period',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='max period'),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='bookings_min_period',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='min period'),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='bookings_min_persons',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='min persons'),
        ),
    ]
