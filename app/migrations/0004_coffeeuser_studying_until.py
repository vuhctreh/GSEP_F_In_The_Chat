# Generated by Django 3.1.6 on 2021-03-03 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210301_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffeeuser',
            name='studying_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]