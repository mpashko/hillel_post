import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hillel_post.settings')

app = Celery('hillel_post', backend='rpc')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_exchange_rates': {
        'task': 'exchanger.tasks.get_exchange_rates',
        'schedule': 10.0
    }
}
