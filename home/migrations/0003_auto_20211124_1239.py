# Generated by Django 3.2.6 on 2021-11-24 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0062_comment_models_and_pagesubscription'),
        ('home', '0002_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_open', models.BooleanField(default=True)),
            ],
            options={
                'permissions': [('manage_attendance', 'Can Manage Attendance System')],
            },
        ),
        migrations.CreateModel(
            name='Collaborators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('icon', models.ImageField(upload_to='collaborators_icons')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='course_thumbnails')),
                ('youtube_link', models.TextField()),
                ('registration_form', models.TextField()),
            ],
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=30)),
                ('duration', models.CharField(max_length=20)),
                ('overview', models.TextField()),
                ('minute', models.TextField()),
                ('minute_file', models.FileField(upload_to='minute_file')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128)),
                ('message', models.TextField()),
                ('has_expired', models.BooleanField(default=False)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('is_pinned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicationSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Symposium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='Symposium_thumbnails')),
                ('youtube_link', models.TextField()),
                ('registration_form', models.TextField()),
            ],
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='Webinar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('thumbnail', models.ImageField(upload_to='webinar_thumbnails')),
                ('youtube_link', models.TextField()),
                ('registration_form', models.TextField()),
            ],
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='designation',
            field=models.CharField(blank=True, default='Member', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='fb_profile_link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='institution',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_core_member',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='ResearchPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date_published', models.DateField()),
                ('is_highlight', models.BooleanField()),
                ('is_completed', models.BooleanField()),
                ('content', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='topics')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image'))], blank=True, null=True)),
                ('refrences', wagtail.core.fields.StreamField([('refrence', wagtail.core.blocks.CharBlock(form_classname='refrence'))], blank=True, null=True)),
                ('view', models.BigIntegerField(default=0)),
                ('author', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('thumbnail', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('content', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True, null=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('sections', models.ManyToManyField(blank=True, to='home.ProjectSection')),
            ],
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_title', models.CharField(max_length=30)),
                ('hod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('issue_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.attendanceissue')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AskForLeaveMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('leave_start_date', models.DateField()),
                ('leave_end_date', models.DateField()),
                ('is_approved', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('manage_attendance', 'Can Manage Attendance System')],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('date_published', models.DateTimeField()),
                ('pdf_file', models.FileField(null=True, upload_to='article_files')),
                ('thumbnail', models.ImageField(null=True, upload_to='article_thumbnails')),
                ('sections', modelcluster.fields.ParentalManyToManyField(blank=True, to='home.PublicationSection')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Absentee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_filled', models.BooleanField(default=False)),
                ('issue_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.attendanceissue')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.department'),
        ),
        migrations.AddConstraint(
            model_name='attendance',
            constraint=models.UniqueConstraint(fields=('issue_date', 'member'), name='unique member and issue_date'),
        ),
    ]
