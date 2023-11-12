from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0026_auto_20231112_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='Group',
            name='listings',
        ),
    ]
