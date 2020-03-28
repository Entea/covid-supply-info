# Generated by Django 3.0.4 on 2020-03-26 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0018_auto_20200327_2329'),
    ]

    operations = [


        migrations.CreateModel(
            name='HospitalNeeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve_amount', models.IntegerField(verbose_name='Reserve amount')),
                ('need_amount', models.IntegerField(verbose_name='Need amount')),
                ('request_amount', models.IntegerField(verbose_name='Request amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='distributor.Hospital', verbose_name='Hospital')),
                ('need_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='distributor.NeedType',
                                                verbose_name='Need Type')),
            ],
        ),
    ]
