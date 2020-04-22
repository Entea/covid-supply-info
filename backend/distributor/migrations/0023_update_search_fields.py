# Generated by Django 3.0.4 on 2020-03-29 10:31

from django.db import migrations, models

from distributor.models import Hospital


def update_hospital_search_fields(apps, schema_editor):
    hospitals = apps.get_model('distributor', 'Hospital').objects.all()
    for hospital in hospitals:
        hospital.save()


class Migration(migrations.Migration):
    dependencies = [
        ('distributor', '0022_auto_20200329_1031'),
    ]

    operations = [
        migrations.RunPython(update_hospital_search_fields),
    ]
