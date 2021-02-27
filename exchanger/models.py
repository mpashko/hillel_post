from django.db import models
from django.utils import timezone


class ExchangeRate(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    currency_a = models.CharField(max_length=3)
    currency_b = models.CharField(max_length=3)
    buy = models.DecimalField(max_digits=8, decimal_places=2)
    sell = models.DecimalField(max_digits=8, decimal_places=2)
    created = models.DateTimeField(default=timezone.now)
