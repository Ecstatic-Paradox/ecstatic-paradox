# Generated by Django 3.2.6 on 2021-12-23 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20211223_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostpage',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
    ]