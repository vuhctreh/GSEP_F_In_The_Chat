# Generated by Django 3.1.6 on 2021-02-18 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210217_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffeeuser',
            name='university',
            field=models.CharField(choices=[('1', 'University of Exeter'), ('2', 'Test uni')], max_length=50),
        ),
    ]
