# Generated by Django 3.2.9 on 2022-08-20 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DailySales', '0006_auto_20220819_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysales',
            name='datepaid',
            field=models.DateField(null=True),
        ),
    ]
