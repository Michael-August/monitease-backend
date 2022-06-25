# Generated by Django 3.2.9 on 2022-06-25 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=80)),
                ('quantity', models.IntegerField()),
                ('restocklevel', models.IntegerField()),
                ('dateadded', models.DateField(auto_now_add=True)),
                ('dateupdated', models.DateField(auto_now=True)),
            ],
        ),
    ]
