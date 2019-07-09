# Generated by Django 2.1.1 on 2019-06-04 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20190605_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exceptionsinfo',
            name='address',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='exceptionsvideo',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='securityguard',
            name='address',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='todoexceptions',
            name='address',
            field=models.CharField(max_length=200),
        ),
    ]
