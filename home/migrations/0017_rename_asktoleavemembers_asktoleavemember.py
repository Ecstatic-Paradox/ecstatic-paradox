# Generated by Django 3.2.3 on 2021-06-16 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_asktoleavemembers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AskToLeaveMembers',
            new_name='AskToLeaveMember',
        ),
    ]