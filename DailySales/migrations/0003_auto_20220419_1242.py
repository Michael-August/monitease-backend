# Generated by Django 3.2.5 on 2022-04-19 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DailySales', '0002_alter_dailysales_itemsold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysales',
            name='datepaid',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='dailysales',
            name='itemsold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soldItem', to='DailySales.itemsold'),
        ),
    ]