# Generated by Django 3.1.13 on 2021-09-04 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfttemplate',
            name='height',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nfttemplate',
            name='width',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
