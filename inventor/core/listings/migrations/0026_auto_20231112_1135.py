# Generated by Django 2.2.14 on 2023-11-12 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0025_auto_20230312_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='weight',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, default=0, help_text='ordering', verbose_name='weight'),
        ),
    ]
