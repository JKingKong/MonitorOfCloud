# Generated by Django 2.1.1 on 2018-12-23 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20181223_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent_comment',
        ),
    ]