# Generated by Django 3.1.13 on 2021-11-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0006_remove_nfttemplate_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfttemplate',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]