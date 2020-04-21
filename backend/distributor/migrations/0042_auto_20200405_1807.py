# Generated by Django 3.0.4 on 2020-04-05 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0041_auto_20200405_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distribution',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distributions', to='distributor.Hospital', verbose_name='Больница'),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='status',
            field=models.CharField(choices=[('ready_to_sent', 'Подготовлено'), ('sent', 'Отправлено'), ('delivered', 'Доставлено')], default='ready_to_sent', max_length=20, verbose_name='Статус'),
        ),
    ]
