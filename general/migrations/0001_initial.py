# Generated by Django 3.0.5 on 2020-04-14 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import general.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('stop_date', models.DateField()),
                ('debit', models.FileField(upload_to='')),
                ('credit', models.FileField(upload_to='')),
            ],
            options={
                'verbose_name': 'agreement',
                'verbose_name_plural': 'agreements',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('New', 'New'), ('Active', 'Active'), ('Reconciliation', 'Reconciliation'), ('Closed', 'Closed')], default=general.models.StatusChoice['NEW'], max_length=32, unique=True)),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('stop_date', models.DateField()),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periods', to='general.Agreement')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.Status')),
            ],
            options={
                'verbose_name': 'period',
                'verbose_name_plural': 'periods',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.Country')),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.AddField(
            model_name='agreement',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='general.Company'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='negotiator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agreements', to=settings.AUTH_USER_MODEL),
        ),
    ]