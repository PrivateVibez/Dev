# Generated by Django 4.2.6 on 2023-10-15 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_privatevibezrevenue_test_fav_buttons_revenue'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatevibezrevenue',
            name='Vibez_To_Dollar',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
