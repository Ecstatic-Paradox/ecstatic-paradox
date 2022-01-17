# Generated by Django 3.2.11 on 2022-01-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_blogpostpage_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fb_profile_link',
        ),
        migrations.AddField(
            model_name='user',
            name='linkedIn_profile',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='personal_website',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
