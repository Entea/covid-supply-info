# Generated by Django 3.0.4 on 2020-04-02 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0033_add_contact_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='code',
            field=models.CharField(help_text='Введите код', max_length=50, unique=True, verbose_name='Код'),
        ),
    ]