# Generated by Django 3.0.5 on 2020-05-07 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Training_and_Placement_app', '0007_auto_20200507_1334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suggested',
            old_name='cmp_id',
            new_name='cmp',
        ),
        migrations.RenameField(
            model_name='suggested',
            old_name='std_id',
            new_name='std',
        ),
    ]
