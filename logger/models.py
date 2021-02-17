from django.db import models


class LogRecord(models.Model):
    path = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    execution_time_sec = models.FloatField()
