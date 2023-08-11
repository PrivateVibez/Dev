# Generated by Django 3.1.5 on 2023-08-11 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20230810_0449'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_Availed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item', models.CharField(blank=True, max_length=200, null=True)),
                ('Cost', models.CharField(blank=True, max_length=200, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='user_data',
            name='Availed',
            field=models.ManyToManyField(blank=True, related_name='Item_Avail', to='accounts.Item_Availed'),
        ),
    ]