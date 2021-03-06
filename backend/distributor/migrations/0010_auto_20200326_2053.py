# Generated by Django 3.0.4 on 2020-03-26 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0009_auto_20200326_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('name_ru', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('name_ky', models.CharField(max_length=200, null=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('name_ru', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('name_ky', models.CharField(max_length=200, null=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.AlterField(
            model_name='donationdetail',
            name='donation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='details', to='distributor.Donation', verbose_name='Donation)'),
        ),
        migrations.AlterField(
            model_name='hospitalphonenumber',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phone_numbers', to='distributor.Hospital', verbose_name='Hospital'),
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('name_ru', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('name_ky', models.CharField(max_length=200, null=True, verbose_name='Name')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distributor.District', verbose_name='District')),
            ],
            options={
                'verbose_name': 'Locality',
                'verbose_name_plural': 'Locality',
            },
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distributor.Region', verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='locality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='distributor.Locality', verbose_name='Locality'),
        ),
    ]
