# Generated by Django 4.1.3 on 2023-04-11 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_rename_hotel_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='Main_Img',
            new_name='Upload_Your_Image',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='name',
            new_name='Username',
        ),
    ]
