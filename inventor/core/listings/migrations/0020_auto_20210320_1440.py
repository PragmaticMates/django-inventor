# Generated by Django 2.2.9 on 2021-03-20 13:40

import django.contrib.postgres.indexes
from django.db import migrations, models
import modeltrans.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0019_auto_20201018_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, help_text='photo or image', max_length=1024, upload_to='images', verbose_name='image')),
                ('banner', models.ImageField(blank=True, help_text='photo or image', max_length=5120, upload_to='banners', verbose_name='banner')),
                ('video_url', models.URLField(max_length=300, verbose_name='video URL')),
                ('i18n', modeltrans.fields.TranslationField(fields=('title', 'description'), required_languages=(), virtual_fields=True)),
                ('listings', models.ManyToManyField(blank=True, related_name='groups', to='listings.Listing', verbose_name='listings')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'ordering': ('title',),
            },
        ),
        migrations.AddIndex(
            model_name='group',
            index=django.contrib.postgres.indexes.GinIndex(fields=['i18n'], name='listings_gr_i18n_effe0d_gin'),
        ),
    ]