# Generated by Django 3.1.13 on 2021-11-10 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0007_auto_20211108_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='sections',
            name='nft_template',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='avatar.nfttemplate'),
            preserve_default=False,
        ),
    ]
