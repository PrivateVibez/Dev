# Generated by Django 3.0.5 on 2023-07-29 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0027_auto_20230729_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_data',
            name='Duration_OHYes_button',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='room_data',
            name='Strength_MMM_button',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='room_data',
            name='Strength_OHYes_button',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='room_data',
            name='Strength_OH_button',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]