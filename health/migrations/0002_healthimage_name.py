# Generated by Django 4.2.16 on 2024-12-04 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthimage',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
