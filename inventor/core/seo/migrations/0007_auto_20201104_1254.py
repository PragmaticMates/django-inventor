# Generated by Django 2.2.4 on 2020-11-04 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('seo', '0006_auto_20201104_1213'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seo',
            unique_together={('content_type', 'object_id', 'path')},
        ),
    ]
