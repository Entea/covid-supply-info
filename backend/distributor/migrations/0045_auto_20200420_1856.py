# Generated by Django 3.0.4 on 2020-04-20 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0044_auto_20200420_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributiondetail',
            name='distribution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distributor.Distribution', verbose_name='Распределение'),
        ),
    ]