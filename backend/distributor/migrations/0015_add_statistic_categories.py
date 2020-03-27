from django.db import migrations, transaction

from distributor.models import StatisticCategory


def add_statistic_categories(apps, schema_editor):
    categories = [
        "Персонала",
        "Волентёров",
        "Коек всего",
        "Обр. по коронавирусу",
        "Больные вирусом в больнице",
        "Выздоровевшие в больнице",
        "Умершие в больнице",
    ]

    with transaction.atomic():
        for category in categories:
            statistic_category = StatisticCategory(name=category, name_ru=category)
            statistic_category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('distributor', '0014_auto_20200327_2104'),
    ]

    operations = [
        migrations.RunPython(add_statistic_categories),
    ]
