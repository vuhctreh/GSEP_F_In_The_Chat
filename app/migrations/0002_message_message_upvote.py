# Generated by Django 3.0.1 on 2021-03-01 06:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_upvote',
            field=models.ManyToManyField(related_name='message_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
