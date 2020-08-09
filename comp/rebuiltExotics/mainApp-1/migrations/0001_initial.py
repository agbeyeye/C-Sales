# Generated by Django 3.0.8 on 2020-07-28 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('sellerType', models.CharField(max_length=60)),
                ('Id', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('make', models.CharField(max_length=60)),
                ('model', models.CharField(max_length=60)),
                ('Year', models.CharField(max_length=60)),
                ('trim', models.CharField(max_length=60)),
                ('engine', models.CharField(max_length=60)),
                ('transmission', models.CharField(max_length=20)),
                ('drivetrain', models.CharField(max_length=60)),
                ('fuelType', models.CharField(max_length=60)),
                ('askingPrice', models.CharField(max_length=60, verbose_name='Asking Price')),
                ('priceNegotiation', models.BooleanField(default=False)),
                ('vin', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=60)),
                ('milleage', models.CharField(max_length=60)),
                ('exteriorColor', models.CharField(max_length=60)),
                ('interiorColor', models.CharField(max_length=60)),
                ('wheelAlignment', models.CharField(max_length=60)),
                ('country', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=60)),
                ('zipCode', models.CharField(max_length=60)),
                ('upgrade', models.TextField(null=True)),
                ('repair', models.TextField(null=True)),
                ('rebuildingLink', models.CharField(max_length=90, null=True)),
                ('recentService', models.TextField(null=True)),
                ('alignmentTest', models.BooleanField(default=False)),
                ('flaws', models.TextField(null=True)),
                ('extraInfo', models.TextField(null=True, verbose_name='Additional Information')),
                ('contact', models.CharField(max_length=30)),
                ('hideContact', models.BooleanField(default=False)),
                ('financing', models.BooleanField(default=False)),
                ('serviceContract', models.BooleanField(default=False)),
                ('termsAndConditionsAccepted', models.BooleanField(default=False)),
                ('views', models.IntegerField()),
                ('date', models.DateField()),
                ('sold', models.BooleanField(default=False)),
                ('seller', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RepairedCarImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/repairs/')),
                ('date', models.DateField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recepientEmail', models.CharField(max_length=60)),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('readStatus', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('readStatus', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/images/')),
                ('date', models.DateField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Car')),
            ],
        ),
    ]
