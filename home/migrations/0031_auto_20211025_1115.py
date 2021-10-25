# Generated by Django 3.2.6 on 2021-10-25 05:30

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_project_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
        migrations.RemoveField(
            model_name='project',
            name='overview',
        ),
        migrations.AddField(
            model_name='article',
            name='pdf_file',
            field=models.FileField(null=True, upload_to='article_files'),
        ),
        migrations.AddField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='article_thumbnails'),
        ),
        migrations.AddField(
            model_name='project',
            name='content',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='something', unique=True),
            preserve_default=False,
        ),
    ]