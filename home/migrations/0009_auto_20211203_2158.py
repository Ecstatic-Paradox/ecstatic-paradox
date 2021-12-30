# Generated by Django 3.2.8 on 2021-12-03 16:13

from django.db import migrations
import home.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20211125_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='content',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', home.models.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='content',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', home.models.ImageChooserBlock(icon='image')), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media'))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='content',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(form_classname='topics')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', home.models.ImageChooserBlock(icon='image'))], blank=True, null=True),
        ),
    ]