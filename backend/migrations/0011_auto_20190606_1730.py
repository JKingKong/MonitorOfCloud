# Generated by Django 2.1.1 on 2019-06-06 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20190605_0004'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExceptionsInfo',
        ),
        migrations.AddField(
            model_name='address',
            name='exception_times',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='exceptionsvideo',
            name='video_path',
            field=models.TextField(default=''),
        ),
    ]
