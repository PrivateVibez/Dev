# Generated by Django 3.0.5 on 2023-08-01 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230730_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
