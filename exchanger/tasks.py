from celery import shared_task
import requests

from exchanger.models import ExchangeRate
from hillel_post.settings import EXCHANGE_RATES_SOURCE

UAH_CODE = 980

CURRENCY_MAP = {
    840: 'USD',
    UAH_CODE: 'UAH',
    978: 'EUR',
    643: 'RUB'
}


@shared_task
def get_exchange_rates():
    print('>> Requesting exchange rates')
    # resp = requests.get(EXCHANGE_RATES_SOURCE)
    # resp = resp.json()
    resp = [
        {
            'currencyCodeA': 840,
            'currencyCodeB': 980,
            'date': 1614204606,
            'rateBuy': 27.85,
            'rateSell': 28.0796
        },
        {
            'currencyCodeA': 978,
            'currencyCodeB': 980,
            'date': 1614249606,
            'rateBuy': 33.8,
            'rateSell': 34.2196
        },
        {
            'currencyCodeA': 643,
            'currencyCodeB': 980,
            'date': 1614204606,
            'rateBuy': 0.36,
            'rateSell': 0.39
        },
        {
            'currencyCodeA': 978,
            'currencyCodeB': 840,
            'date': 1614250206,
            'rateBuy': 1.212,
            'rateSell': 1.225
        },
        {
            'currencyCodeA': 985,
            'currencyCodeB': 980,
            'date': 1614254750,
            'rateBuy': 7.5,
            'rateSell': 7.66,
            'rateCross': 7.6599
        }
    ]
    exchange_rates = [get_exchange_rate(d) for d in filter_out_rates(resp)]
    ExchangeRate.objects.all().delete()
    ExchangeRate.objects.bulk_create(exchange_rates)
    return exchange_rates


def filter_out_rates(rates):
    for r in rates:
        currency_a = r['currencyCodeA']
        if currency_a not in CURRENCY_MAP:
            continue
        currency_b = r['currencyCodeB']
        if currency_b not in CURRENCY_MAP:
            continue
        if currency_a != UAH_CODE and currency_b != UAH_CODE:
            continue
        r['currency_a'] = CURRENCY_MAP[currency_a]
        r['currency_b'] = CURRENCY_MAP[currency_b]
        yield r


def get_exchange_rate(rate):
    currency_a = rate['currency_a']
    currency_b = rate['currency_b']
    return ExchangeRate(
        id=currency_a + currency_b,
        currency_a=currency_a,
        currency_b=currency_b,
        buy=rate['rateBuy'],
        sell=rate['rateSell']
    )
