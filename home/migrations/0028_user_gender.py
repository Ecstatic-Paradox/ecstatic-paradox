# Generated by Django 3.2.6 on 2021-10-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20211018_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]