# Generated by Django 3.1.6 on 2021-04-07 19:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('currency_a', models.CharField(max_length=3)),
                ('currency_b', models.CharField(max_length=3)),
                ('buy', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sell', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
