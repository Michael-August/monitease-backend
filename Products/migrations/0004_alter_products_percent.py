# Generated by Django 3.2.9 on 2022-10-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_products_total_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='percent',
            field=models.IntegerField(default=0),
        ),
    ]
