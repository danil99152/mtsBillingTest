# Generated by Django 4.2.2 on 2023-06-30 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msisdn', models.CharField(max_length=255)),
                ('dialed', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('circuit_in', models.CharField(max_length=255)),
                ('circuit_out', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('file_index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_index', models.IntegerField()),
                ('prefix_zones', models.CharField(max_length=255)),
                ('duration', models.IntegerField()),
            ],
        ),
    ]
