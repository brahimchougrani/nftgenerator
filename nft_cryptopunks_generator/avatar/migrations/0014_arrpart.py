# Generated by Django 3.1.13 on 2021-11-19 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0013_auto_20211119_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrpart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arr', models.TextField()),
                ('nft_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avatar.nfttemplate')),
            ],
        ),
    ]
