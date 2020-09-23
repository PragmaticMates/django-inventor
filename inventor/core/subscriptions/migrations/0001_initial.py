# Generated by Django 2.2.4 on 2020-09-23 06:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('order', models.PositiveSmallIntegerField(default=1, help_text='to set order in pricing', unique=True, verbose_name='ordering')),
                ('trial_duration', models.PositiveSmallIntegerField(default=0, help_text='in days', verbose_name='trial duration')),
                ('is_default', models.BooleanField(db_index=True, default=False, help_text='Default plan for user')),
                ('is_available', models.BooleanField(db_index=True, default=False, help_text='Is still available for purchase', verbose_name='available')),
                ('is_visible', models.BooleanField(db_index=True, default=True, help_text='Is visible in current offer', verbose_name='visible')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'plan',
                'verbose_name_plural': 'plans',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='codename')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('unit', models.CharField(blank=True, max_length=100, verbose_name='unit')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('is_boolean', models.BooleanField(default=False, verbose_name='is boolean')),
            ],
            options={
                'verbose_name': 'Quota',
                'verbose_name_plural': 'Quotas',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration', models.DateField(blank=True, db_index=True, default=None, null=True, verbose_name='Expires')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan', verbose_name='plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User plan',
                'verbose_name_plural': 'Users plans',
            },
        ),
        migrations.CreateModel(
            name='PricingPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(blank=True, choices=[('DAY', 'day'), ('MONTH', 'month'), ('YEAR', 'year')], max_length=5, verbose_name='period')),
                ('duration', models.PositiveSmallIntegerField(blank=True, default=None, help_text='in period', null=True, verbose_name='duration')),
                ('price', models.DecimalField(blank=True, db_index=True, decimal_places=2, default=None, help_text='EUR', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='price')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan')),
            ],
            options={
                'verbose_name': 'pricing plan',
                'verbose_name_plural': 'pricing plans',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='PlanQuota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(blank=True, default=1, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan')),
                ('quota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Quota')),
            ],
            options={
                'verbose_name': 'Plan quota',
                'verbose_name_plural': 'Plans quotas',
            },
        ),
        migrations.AddField(
            model_name='plan',
            name='quotas',
            field=models.ManyToManyField(through='subscriptions.PlanQuota', to='subscriptions.Quota'),
        ),
    ]
