# Generated by Django 2.1.1 on 2019-06-06 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_address_threshold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exceptionsvideo',
            name='video_path',
            field=models.TextField(default='null'),
        ),
    ]