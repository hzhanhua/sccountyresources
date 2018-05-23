# Generated by Django 2.0.2 on 2018-05-17 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=100)),
                ('calendar_id', models.CharField(max_length=100)),
                ('iso_date_time', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=13)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sccalendar.Event')),
            ],
        ),
    ]
