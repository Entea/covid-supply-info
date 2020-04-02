import csv
import os

from django.db import migrations, transaction

from distributor.models import Hospital, Statistic, StatisticCategory


def clean_row(row):
    for index, value in enumerate(row):
        if value:
            row[index] = value.strip()
    return row


def convert_to_int(string):
    try:
        return int(string), True
    except:
        return None, False


def add_statistics(apps, schema_editor):
    beds_statistic_category = StatisticCategory.objects.get(name='Коек всего')
    doctors_statistic_category = StatisticCategory.objects.get(name='Врачи')
    nurses_statistic_category = StatisticCategory.objects.get(name='Средний медперсонал')

    file_path = os.path.dirname(os.path.realpath(__file__)) + '/files/20200402-hospital-statistics.csv'
    with open(file_path, newline='') as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar="'")
        next(csv_reader)
        for row in csv_reader:
            code, beds, doctors, nurses = clean_row(row)
            hospital = Hospital.objects.filter(code=code).first()
            if not hospital:
                continue

            beds, ok = convert_to_int(beds)
            if ok:
                with transaction.atomic():
                    Statistic.objects.update_or_create(hospital=hospital,
                                                       category=beds_statistic_category,
                                                       defaults={
                                                           'actual': beds
                                                       })
                    print("Beds statistic has been updated for hospital {}".format(hospital))

            doctors, ok = convert_to_int(doctors)
            if ok:
                with transaction.atomic():
                    Statistic.objects.update_or_create(hospital=hospital,
                                                       category=doctors_statistic_category,
                                                       defaults={
                                                           'actual': doctors
                                                       })
                    print("Doctors statistic has been updated for hospital {}".format(hospital))

            nurses, ok = convert_to_int(nurses)
            if ok:
                with transaction.atomic():
                    Statistic.objects.update_or_create(hospital=hospital,
                                                       category=nurses_statistic_category,
                                                       defaults={
                                                           'actual': nurses
                                                       })
                    print("Nurses statistic has been updated for hospital {}".format(hospital))


class Migration(migrations.Migration):
    dependencies = [
        ('distributor', '0036_add_statistic_category'),
    ]

    operations = [
        migrations.RunPython(add_statistics),
    ]
