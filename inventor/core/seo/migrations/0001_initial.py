# Generated by Django 2.2.4 on 2020-07-06 18:34

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import modeltrans.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=200, verbose_name='title')),
                ('description', models.CharField(blank=True, default='', max_length=200, verbose_name='description')),
                ('keywords', models.CharField(blank=True, default='', max_length=1000, verbose_name='keywords')),
                ('object_id', models.PositiveIntegerField()),
                ('i18n', modeltrans.fields.TranslationField(fields=('title', 'description', 'keywords'), required_languages=(), virtual_fields=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'SEO fields',
                'verbose_name_plural': 'SEO fields',
            },
        ),
        migrations.AddIndex(
            model_name='seo',
            index=django.contrib.postgres.indexes.GinIndex(fields=['i18n'], name='seo_seo_i18n_9f53d0_gin'),
        ),
        migrations.AlterUniqueTogether(
            name='seo',
            unique_together={('content_type', 'object_id')},
        ),
    ]
