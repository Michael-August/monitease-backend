# Generated by Django 3.2.9 on 2022-08-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DailySales', '0005_auto_20220818_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysales',
            name='dateupdated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='dailysales',
            name='datepaid',
            field=models.DateField(),
        ),
    ]
