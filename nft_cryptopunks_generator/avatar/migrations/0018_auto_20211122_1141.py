# Generated by Django 3.1.13 on 2021-11-22 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0017_images_exclude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='exclude',
            field=models.ManyToManyField(related_name='_images_exclude_+', to='avatar.Images'),
        ),
    ]
