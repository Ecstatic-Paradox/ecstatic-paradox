# Generated by Django 3.2.11 on 2022-01-17 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20220117_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='priority_order',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
