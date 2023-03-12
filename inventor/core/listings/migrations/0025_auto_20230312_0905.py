# Generated by Django 2.2.14 on 2023-03-12 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0024_auto_20211219_1911'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('weight', 'title'), 'verbose_name': 'group', 'verbose_name_plural': 'groups'},
        ),
        migrations.AddField(
            model_name='group',
            name='weight',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, default=0, help_text='ordering', null=True, verbose_name='weight'),
        ),
    ]
