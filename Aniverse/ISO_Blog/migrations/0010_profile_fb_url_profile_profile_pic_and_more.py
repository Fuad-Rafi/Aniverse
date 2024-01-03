# Generated by Django 4.2.7 on 2023-12-04 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISO_Blog', '0009_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fb_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile'),
        ),
    ]