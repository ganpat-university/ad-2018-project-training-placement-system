# Generated by Django 3.0.5 on 2020-05-08 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training_and_Placement_app', '0008_auto_20200507_1442'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='aadhar_number',
            new_name='aadhaar_number',
        ),
        migrations.AddField(
            model_name='company',
            name='hired_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]