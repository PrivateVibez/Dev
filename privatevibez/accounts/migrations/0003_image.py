# Generated by Django 3.0.5 on 2022-12-28 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20221227_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='temp')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
