# Generated by Django 4.1.7 on 2023-03-04 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ava',
            field=models.ImageField(default='users/default_ava.jpg', upload_to='users/avatars/%Y/%m/%d/'),
        ),
    ]
