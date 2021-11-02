# Generated by Django 3.2.7 on 2021-10-31 23:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20211031_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='_network_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
