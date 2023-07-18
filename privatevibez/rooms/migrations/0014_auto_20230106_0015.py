# Generated by Django 3.0.5 on 2023-01-06 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0013_bad_acters_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('Broacaster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Broacaster', to=settings.AUTH_USER_MODEL)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room_Sesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='five_dice_Name',
            new_name='Five_Dice_Name',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='five_dice_Time',
            new_name='Five_Dice_Time',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='four_dice_Name',
            new_name='Four_Dice_Name',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='four_dice_Time',
            new_name='Four_Dice_Time',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='one_dice_Name',
            new_name='One_Dice_Name',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='one_dice_Time',
            new_name='One_Dice_Time',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='six_dice_Name',
            new_name='Six_Dice_Name',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='six_dice_Time',
            new_name='Six_Dice_Time',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='three_dice_Name',
            new_name='Three_Dice_Name',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='three_dice_Time',
            new_name='Three_Dice_Time',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='two_dice_Name',
            new_name='Two_Dice_Name',
        ),
        migrations.RenameField(
            model_name='dice_data',
            old_name='two_dice_Time',
            new_name='Two_Dice_Time',
        ),
        migrations.RenameField(
            model_name='menu_data',
            old_name='timestamp',
            new_name='Timestamp',
        ),
        migrations.RenameField(
            model_name='room_data',
            old_name='timestamp',
            new_name='Timestamp',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Age',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Body_Type',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Follow',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='I_Am',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Interested_In',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Language',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Location',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Profile_Pic',
        ),
        migrations.RemoveField(
            model_name='room_data',
            name='Real_Name',
        ),
        migrations.DeleteModel(
            name='Bad_Acters',
        ),
    ]
