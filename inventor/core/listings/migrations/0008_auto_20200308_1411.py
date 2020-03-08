# Generated by Django 2.2.4 on 2020-03-08 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_accommodation_rooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='bookings_enabled',
            field=models.BooleanField(default=True, verbose_name='bookings enabled'),
        ),
        migrations.AddField(
            model_name='accommodation',
            name='capacity',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='capacity'),
        ),
    ]
