# Generated by Django 4.2.7 on 2024-04-08 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='ip_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]