# Generated by Django 3.0.5 on 2023-01-23 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist_dev',
            name='Staff',
        ),
        migrations.RemoveField(
            model_name='todoproject_dev',
            name='Staff',
        ),
    ]
