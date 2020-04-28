from django.db import migrations, transaction
from django.db.models import Q


def fix_statistics(apps, schema_editor):
    with transaction.atomic():
        Statistic = apps.get_model('distributor', 'Statistic')
        statistics = Statistic.objects.filter(Q(has_capacity=True) & Q(capacity=None))
        for statistic in statistics:
            statistic.has_capacity = False
            statistic.save()


class Migration(migrations.Migration):
    dependencies = [
        ('distributor', '0054_auto_20200426_1123'),
    ]

    operations = [
        migrations.RunPython(fix_statistics)
    ]
