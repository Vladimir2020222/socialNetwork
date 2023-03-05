# Generated by Django 4.1.7 on 2023-03-05 18:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_age_user_date_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscriptions',
            field=models.ManyToManyField(related_name='subscribers', related_query_name='subscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]
