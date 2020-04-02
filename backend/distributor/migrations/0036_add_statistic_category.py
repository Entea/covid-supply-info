from django.db import migrations


def add_statistic_category(apps, schema_editor):
    StatisticCategory = apps.get_model('distributor', 'StatisticCategory')

    try:
        statistic_category = StatisticCategory.objects.get(name='Персонала')
        statistic_category.name = 'Врачи'
        statistic_category.save()
    except StatisticCategory.DoesNotExist:
        print("CategoryStatistic with name {} not found".format('Персонала'))

    StatisticCategory.objects.create(name='Средний медперсонал', name_ru='Средний медперсонал')


class Migration(migrations.Migration):
    dependencies = [
        ('distributor', '0035_import_hospitals_addresses'),
    ]

    operations = [
        migrations.RunPython(add_statistic_category),
    ]
