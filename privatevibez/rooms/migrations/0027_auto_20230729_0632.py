# Generated by Django 3.0.5 on 2023-07-29 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0026_auto_20230729_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_data',
            name='Feature_MMM_button',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='room_data',
            name='Feature_OHYes_button',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='room_data',
            name='Feature_OH_button',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
