# Generated by Django 2.0.5 on 2018-05-10 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=10)),
                ('seat_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('land_date', models.DateTimeField()),
                ('start_airport', models.CharField(max_length=20)),
                ('land_airport', models.CharField(max_length=20)),
                ('airplane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightmanager.Airplane')),
            ],
        ),
        migrations.CreateModel(
            name='Passanger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('luggage_weight', models.IntegerField()),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightmanager.Flight')),
                ('passanger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightmanager.Passanger')),
            ],
        ),
    ]
