# Generated by Django 3.1.13 on 2021-09-04 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gb_used',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
