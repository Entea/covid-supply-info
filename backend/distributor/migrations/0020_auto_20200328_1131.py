# Generated by Django 3.0.4 on 2020-03-28 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0019_auto_20200328_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalneeds',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='needs', to='distributor.Hospital', verbose_name='Hospital'),
        ),
    ]