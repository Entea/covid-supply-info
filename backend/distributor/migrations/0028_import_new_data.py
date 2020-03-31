# Generated by Django 3.0.4 on 2020-03-31 14:56
from django.db import migrations, transaction

from distributor.models import Hospital, Statistic, StatisticCategory
from csv import reader
import os


def import_new_stuff(apps, schema_editor):
    try:
        stat_cat = StatisticCategory.objects.get(name='Коек всего')

        with open(os.path.dirname(os.path.realpath(__file__)) + '/files/beds.csv', newline='') as file:
            csvin = reader(file, delimiter=',')
            for row in csvin:
                hospital_code = None
                number_of_beds = None
                try:
                    hospital_code = str(row[0]).strip()
                    number_of_beds = int(str(row[1]).strip())
                except Exception as e:
                    print("Error occurred during casting", e)
                if hospital_code and number_of_beds >= 0:
                    print("Hospital code = {}, # of beds = {}".format(hospital_code, number_of_beds))
                    try:
                        hospital = Hospital.objects.get(code=hospital_code)
                        with transaction.atomic():
                            stat_entry, created = Statistic.objects.get_or_create(hospital=hospital,
                                                                                  category=stat_cat,
                                                                                  actual=number_of_beds)
                            stat_entry.save()
                        print("Update hospital {} statistic {}".format(hospital, created))
                    except Hospital.DoesNotExist:
                        print('Hospital not found', hospital_code)
                else:
                    print("Invalid data: hospital code = {}, # of beds = {}", hospital_code, number_of_beds)
    except Exception as e:
        print("Error happened during migration", e)


class Migration(migrations.Migration):
    dependencies = [
        ('distributor', '0027_auto_20200330_1631'),
    ]

    operations = [
        migrations.RunPython(import_new_stuff),
    ]
