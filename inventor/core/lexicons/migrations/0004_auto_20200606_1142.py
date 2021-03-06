# Generated by Django 2.2.4 on 2020-06-06 09:42

import colorful.fields
from django.db import migrations
import modeltrans.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lexicons', '0003_auto_20200603_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=colorful.fields.RGBColorField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='category',
            name='i18n',
            field=modeltrans.fields.TranslationField(fields=('title', 'slug'), required_languages=(), virtual_fields=True),
        ),
    ]
