# Generated by Django 2.2.4 on 2020-09-03 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0002_auto_20191127_1542'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscription',
            new_name='Subscriber',
        ),
        migrations.AlterModelOptions(
            name='subscriber',
            options={'ordering': ['email'], 'verbose_name': 'subscriber', 'verbose_name_plural': 'subscribers'},
        ),
    ]
