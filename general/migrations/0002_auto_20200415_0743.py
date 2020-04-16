# Generated by Django 3.0.5 on 2020-04-15 07:43

from django.db import migrations

from general.models import StatusChoice


def generate_statuses(apps, schema_editor):
    Status = apps.get_model('general', 'Status')
    statuses = []
    for status in StatusChoice:
        statuses.append(Status(name=status.value))
    Status.objects.bulk_create(statuses, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_statuses)
    ]