from django.db import models
from django.utils import timezone


class ExchangeRate(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    currency_a = models.CharField(max_length=3)
    currency_b = models.CharField(max_length=3)
    buy = models.DecimalField(max_digits=8, decimal_places=2)
    sell = models.DecimalField(max_digits=8, decimal_places=2)
    created = models.DateTimeField(default=timezone.now)

    def to_dict(self):
        currency_a = self.currency_a.lower()
        return {
            f'{currency_a}_buy': self.buy,
            f'{currency_a}_sell': self.sell
        }

    def __str__(self):
        return f'currency_a={self.currency_a}, buy={self.buy}, ' \
               f'sell={self.sell}'
