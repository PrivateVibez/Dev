# Generated by Django 3.0.5 on 2023-08-02 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='Status',
            field=models.CharField(blank=True, default='User', max_length=20, null=True),
        ),
    ]