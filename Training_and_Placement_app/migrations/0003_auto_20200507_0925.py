# Generated by Django 3.0.5 on 2020-05-07 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Training_and_Placement_app', '0002_company_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='hired_count',
        ),
        migrations.AddField(
            model_name='company',
            name='package',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='criteria',
            field=models.FloatField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='other_details',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
    ]
