# Generated by Django 4.2.16 on 2024-12-14 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0003_fitnessrecord_delete_healthimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnessrecord',
            name='bmi',
        ),
        migrations.RemoveField(
            model_name='fitnessrecord',
            name='cholesterol_level',
        ),
        migrations.RemoveField(
            model_name='fitnessrecord',
            name='hemoglobin_level',
        ),
        migrations.RemoveField(
            model_name='fitnessrecord',
            name='pulse_rate',
        ),
        migrations.RemoveField(
            model_name='fitnessrecord',
            name='sugar_level',
        ),
        migrations.RemoveField(
            model_name='fitnessrecord',
            name='uric_acid_level',
        ),
        migrations.AlterField(
            model_name='fitnessrecord',
            name='age',
            field=models.CharField(max_length=50),
        ),
    ]
