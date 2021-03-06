# Generated by Django 3.1.13 on 2021-09-04 07:23

from django.db import migrations, models
import django.db.models.deletion
import django_validated_jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedArray',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django_validated_jsonfield.fields.ValidatedJSONField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='NftTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('image', models.ImageField(upload_to='')),
                ('variants', models.IntegerField()),
                ('variants_used', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('position_x', models.FloatField()),
                ('position_y', models.FloatField()),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('raretiy', models.IntegerField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avatar.sections')),
            ],
        ),
    ]
