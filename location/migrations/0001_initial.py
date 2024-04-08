# Generated by Django 4.2.7 on 2024-04-03 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('ip_address', models.CharField(max_length=255)),
                ('booth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.booth')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location')),
            ],
        ),
        migrations.AddField(
            model_name='booth',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.location'),
        ),
    ]
