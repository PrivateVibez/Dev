# Generated by Django 3.0.5 on 2022-12-29 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20221229_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data',
            name='Id_file',
            field=models.ImageField(upload_to='ID'),
        ),
    ]
