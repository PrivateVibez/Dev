# Generated by Django 3.1.5 on 2023-09-01 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_item_availed_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Cost', models.CharField(blank=True, max_length=200, null=True)),
                ('Vibez', models.IntegerField(blank=True, default=0, null=True)),
                ('Slots', models.IntegerField(blank=True, default=0, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user_data',
            name='Subscription_Type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.subscription'),
        ),
    ]
