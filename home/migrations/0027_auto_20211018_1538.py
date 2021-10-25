# Generated by Django 3.2.6 on 2021-10-18 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20211018_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaborators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('icon', models.ImageField(upload_to='collaborators_icons')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_core_member',
            field=models.BooleanField(default=True),
        ),
    ]