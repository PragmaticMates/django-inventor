# Generated by Django 2.2.4 on 2020-03-09 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20200308_1327'),
        ('listings', '0014_auto_20200308_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'shop',
                'verbose_name_plural': 'shops',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
        migrations.DeleteModel(
            name='Goods',
        ),
    ]
