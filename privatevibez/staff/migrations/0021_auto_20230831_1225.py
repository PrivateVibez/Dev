# Generated by Django 3.1.5 on 2023-08-31 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0020_privatevibezrevenue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='privatevibezrevenue',
            old_name='Slot_Machine_Spin_Cost',
            new_name='Chargeback',
        ),
    ]