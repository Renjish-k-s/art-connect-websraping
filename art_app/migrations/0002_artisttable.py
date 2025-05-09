# Generated by Django 5.1.6 on 2025-02-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artisttable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='uploads/')),
                ('name', models.CharField(max_length=30)),
                ('bio', models.TextField(max_length=100)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=50)),
                ('insta', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=60)),
                ('art_cat', models.CharField(max_length=30)),
            ],
        ),
    ]
