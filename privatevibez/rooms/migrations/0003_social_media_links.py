# Generated by Django 4.2.6 on 2023-10-08 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Social_Media_Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Social_Media', models.CharField(blank=True, max_length=200, null=True)),
                ('Link', models.CharField(blank=True, max_length=200, null=True)),
                ('Vibez_Cost', models.IntegerField(blank=True, default=0, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
