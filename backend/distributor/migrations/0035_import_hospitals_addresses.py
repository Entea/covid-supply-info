import csv
import os

from django.db import migrations


def clean_row(row):
    for index, value in enumerate(row):
        if value:
            row[index] = value.strip()
    return row


def import_hospitals_addresses(apps, schema_editor):
    Hospital = apps.get_model('distributor', 'Hospital')

    file_path = os.path.dirname(os.path.realpath(__file__)) + '/files/20200402-hospital-addresses.csv'
    with open(file_path, newline='') as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar="'")
        next(csv_reader)
        for row in csv_reader:
            code, _, _, address = clean_row(row)
            if address and code:
                hospital = Hospital.objects.filter(code=code).first()
                if hospital:
                    hospital.address = address
                    hospital.save()


class Migration(migrations.Migration):
    dependencies = [
        ('distributor', '0034_auto_20200402_1233'),
    ]

    operations = [
        migrations.RunPython(import_hospitals_addresses),
    ]
