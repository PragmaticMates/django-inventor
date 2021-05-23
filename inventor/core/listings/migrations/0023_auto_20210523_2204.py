# Generated by Django 2.2.14 on 2021-05-23 20:04

from django.db import migrations
import modeltrans.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0022_group_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='i18n',
            field=modeltrans.fields.TranslationField(fields=('slug', 'title', 'description'), required_languages=(), virtual_fields=True),
        ),
    ]
