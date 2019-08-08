# Generated by Django 2.2.4 on 2019-08-08 14:52

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.hstore
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import internationalflavor.countries.models
import inventor.core.bookings.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('listing_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='listing type')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('listing_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='listing type')),
            ],
            options={
                'verbose_name': 'feature',
                'verbose_name_plural': 'features',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('published', models.BooleanField(default=True, verbose_name='published')),
                ('promoted', models.BooleanField(default=False, verbose_name='promoted')),
                ('price_starts_at', models.BooleanField(default=False, verbose_name='price starts at')),
                ('price', models.DecimalField(blank=True, db_index=True, decimal_places=2, default=None, help_text='€', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price')),
                ('price_unit', models.CharField(blank=True, choices=[('PERSON', 'person'), ('DAY', 'day'), ('NIGHT', 'night'), ('PERSON_NIGHT', 'person per night')], max_length=6, verbose_name='price per unit')),
                ('street', models.CharField(blank=True, max_length=200, verbose_name='street')),
                ('postcode', models.CharField(blank=True, max_length=30, verbose_name='postcode')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='city')),
                ('country', internationalflavor.countries.models.CountryField(blank=True, db_index=True, verbose_name='country')),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, db_index=True, default=None, null=True, srid=4326, verbose_name='point')),
                ('image', models.ImageField(blank=True, help_text='photo or image', max_length=1024, upload_to='images', verbose_name='image')),
                ('banner', models.ImageField(blank=True, help_text='photo or image', max_length=5120, upload_to='banners', verbose_name='banner')),
                ('person', models.CharField(blank=True, max_length=100, verbose_name='person')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('website', models.URLField(blank=True, max_length=400, verbose_name='website')),
                ('social_networks', django.contrib.postgres.fields.hstore.HStoreField(blank=True, verbose_name='social networks')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('categories', models.ManyToManyField(blank=True, related_name='listings_of_category', to='listings.Category', verbose_name='categories')),
                ('features', models.ManyToManyField(blank=True, related_name='listings_with_features', to='listings.Feature', verbose_name='features')),
            ],
            options={
                'verbose_name': 'listing',
                'verbose_name_plural': 'listings',
                'db_table': 'listings_general',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'accommodation',
                'verbose_name_plural': 'accommodations',
                'ordering': ('title',),
            },
            bases=(inventor.core.bookings.mixins.BookingMixin, 'listings.listing'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='EatAndDrink',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'eat & drink',
                'verbose_name_plural': 'eat & drinks',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'goods',
                'verbose_name_plural': 'goods',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'job',
                'verbose_name_plural': 'jobs',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Nature',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'animal or plant',
                'verbose_name_plural': 'animals and plants',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'business',
                'verbose_name_plural': 'businesses',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'travel',
                'verbose_name_plural': 'travels',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'vehicle',
                'verbose_name_plural': 'vehicle',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('url', models.URLField(max_length=300, verbose_name='URL')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'video',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(help_text='photo, image or icon', max_length=5120, upload_to='photos', verbose_name='file')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.Album')),
            ],
            options={
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='listing',
            name='location',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.Location'),
        ),
        migrations.AddField(
            model_name='album',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.Listing'),
        ),
    ]
