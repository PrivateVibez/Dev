# Generated by Django 4.2.5 on 2023-09-25 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0031_alter_decline_message_id_alter_memos_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block_Ip_Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Games_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Slot_Machine_Spin_Cost', models.IntegerField(blank=True, null=True)),
                ('Lottery_Spin_Cost', models.IntegerField(blank=True, null=True)),
                ('Dice_Spin_Cost', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slot_Machine_limit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number_of_Three_of_a_kind_winners', models.IntegerField(blank=True, null=True)),
                ('Number_of_Two_of_a_kind_winners', models.IntegerField(blank=True, null=True)),
                ('Number_of_Three_of_a_kind_losers', models.IntegerField(blank=True, null=True)),
                ('Number_of_Two_of_a_kind_losers', models.IntegerField(blank=True, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thumbs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Thumb', models.CharField(blank=True, max_length=200, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('Broadcaster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Thumb_Broadcaster', to=settings.AUTH_USER_MODEL)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Slot_Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Slot_cost_per_spin', models.IntegerField(blank=True, null=True)),
                ('Win_3_of_a_kind_prize', models.CharField(blank=True, max_length=200, null=True)),
                ('Win_2_of_a_kind_prize', models.CharField(blank=True, max_length=200, null=True)),
                ('Prize', models.CharField(blank=True, max_length=200, null=True)),
                ('pot', models.IntegerField(blank=True, default=0, null=True)),
                ('pot_increase', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(null=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room_Visitors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room_Sesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Goal_Currrent', models.IntegerField(blank=True, default=0, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tab', models.CharField(blank=True, max_length=200, null=True)),
                ('Goal', models.IntegerField(blank=True, default=0, null=True)),
                ('Public_Chat', models.BooleanField(default=True)),
                ('Private_Chat', models.BooleanField(default=True)),
                ('Private_Chat_Price', models.IntegerField(blank=True, default=0, null=True)),
                ('Price_MMM_button', models.IntegerField(blank=True, default=10, null=True)),
                ('Price_OH_button', models.IntegerField(blank=True, default=50, null=True)),
                ('Price_OHYes_button', models.IntegerField(blank=True, default=75, null=True)),
                ('Duration_MMM_button', models.IntegerField(blank=True, default=1, null=True)),
                ('Duration_OH_button', models.IntegerField(blank=True, default=2, null=True)),
                ('Duration_OHYes_button', models.IntegerField(blank=True, default=3, null=True)),
                ('Strength_MMM_button', models.CharField(blank=True, max_length=100, null=True)),
                ('Strength_OH_button', models.CharField(blank=True, max_length=100, null=True)),
                ('Strength_OHYes_button', models.CharField(blank=True, max_length=100, null=True)),
                ('Feature_OHYes_button', models.CharField(blank=True, max_length=1, null=True)),
                ('Feature_OH_button', models.CharField(blank=True, max_length=1, null=True)),
                ('Feature_MMM_button', models.CharField(blank=True, max_length=1, null=True)),
                ('Is_Active', models.BooleanField(default=False)),
                ('hashtags', models.TextField(blank=True, null=True)),
                ('Room_Rules', models.TextField(blank=True, null=True)),
                ('Room_Description', models.TextField(blank=True, null=True)),
                ('Revenue', models.IntegerField(blank=True, default=0, null=True)),
                ('Is_Dice_Active', models.BooleanField(default=False)),
                ('Is_Menu_Active', models.BooleanField(default=False)),
                ('Is_Lottery_Active', models.BooleanField(default=False)),
                ('Total_Viewers', models.IntegerField(blank=True, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('Room_promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_promotion', to='staff.promotion')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Visitors', models.ManyToManyField(blank=True, null=True, to='rooms.room_visitors')),
            ],
        ),
        migrations.CreateModel(
            name='Menu_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Vibez_Cost', models.IntegerField(blank=True, null=True)),
                ('Menu_Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Menu_Time', models.CharField(blank=True, max_length=200, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_number', models.IntegerField(blank=True, null=True)),
                ('prize', models.CharField(blank=True, max_length=200, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('Broadcaster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Broadcaster', to=settings.AUTH_USER_MODEL)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dice_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('One_Dice_Name', models.CharField(blank=True, max_length=200, null=True)),
                ('One_Dice_Time', models.IntegerField(blank=True, null=True)),
                ('Two_Dice_Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Two_Dice_Time', models.IntegerField(blank=True, null=True)),
                ('Three_Dice_Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Three_Dice_Time', models.IntegerField(blank=True, null=True)),
                ('Four_Dice_Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Four_Dice_Time', models.IntegerField(blank=True, null=True)),
                ('Five_Dice_Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Five_Dice_Time', models.IntegerField(blank=True, null=True)),
                ('Six_Dice_Name', models.CharField(blank=True, max_length=200, null=True)),
                ('Six_Dice_Time', models.IntegerField(blank=True, null=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dice_number', models.IntegerField(blank=True, null=True)),
                ('prize', models.CharField(blank=True, max_length=200, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
