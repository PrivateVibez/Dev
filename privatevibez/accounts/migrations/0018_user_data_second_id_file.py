# Generated by Django 3.1.5 on 2023-09-08 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_subscription_badge'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='Second_Id_File',
            field=models.ImageField(blank=True, null=True, upload_to='2nd_ID'),
        ),
    ]