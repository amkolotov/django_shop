# Generated by Django 3.1.2 on 2020-10-24 09:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20201020_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 26, 9, 46, 57, 125179, tzinfo=utc)),
        ),
    ]
