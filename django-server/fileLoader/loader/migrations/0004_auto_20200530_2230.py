# Generated by Django 3.0.6 on 2020-05-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loader', '0003_auto_20200530_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='transaction_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='financial_data',
            name='transaction_time',
            field=models.DateTimeField(),
        ),
    ]
