# Generated by Django 2.2.14 on 2021-05-23 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewcomment',
            name='type',
        ),
    ]