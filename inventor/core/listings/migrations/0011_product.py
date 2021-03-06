# Generated by Django 2.2.4 on 2020-06-18 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0010_auto_20200618_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('listing_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='listings.Listing')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('title',),
            },
            bases=('listings.listing',),
        ),
    ]
