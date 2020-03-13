# Generated by Django 2.2.4 on 2020-03-12 23:05

from django.db import migrations, models
import django.db.models.deletion
import inventor.core.listings.mixins
import mptt.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccommodationAmenity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('slug', models.SlugField(default='', max_length=150, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'accommodation amenity',
                'verbose_name_plural': 'accommodation amenities',
                'ordering': ('title',),
            },
            bases=(inventor.core.listings.mixins.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('slug', models.SlugField(default='', max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'feature',
                'verbose_name_plural': 'features',
                'ordering': ('title',),
            },
            bases=(inventor.core.listings.mixins.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('slug', models.SlugField(default='', max_length=150, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('photo', sorl.thumbnail.fields.ImageField(blank=True, default=None, max_length=5120, null=True, upload_to='localities', verbose_name='photo')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='lexicons.Locality')),
            ],
            options={
                'verbose_name': 'locality',
                'verbose_name_plural': 'localities',
                'ordering': ('title',),
            },
            bases=(inventor.core.listings.mixins.SlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(default='', max_length=150, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('listing_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType', verbose_name='listing type')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='lexicons.Category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
                'unique_together': {('title', 'listing_type')},
            },
            bases=(inventor.core.listings.mixins.SlugMixin, models.Model),
        ),
    ]
