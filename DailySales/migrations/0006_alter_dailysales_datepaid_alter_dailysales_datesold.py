# Generated by Django 4.0.4 on 2022-05-13 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DailySales', '0005_rename_itemsold_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysales',
            name='datepaid',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='dailysales',
            name='datesold',
            field=models.DateField(auto_now_add=True),
        ),
    ]
