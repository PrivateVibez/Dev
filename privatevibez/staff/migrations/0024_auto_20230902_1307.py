# Generated by Django 3.1.5 on 2023-09-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0023_privatevibezrevenue_vibe_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatevibezrevenue',
            name='Vibe_Cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
