from django.db import models


class Sighting(models.Model):
    host = models.CharField(max_length=32)
    device_id = models.CharField(max_length=32)
    signal_dbm = models.IntegerField()
    timestamp = models.IntegerField()
    processed = models.BooleanField(default=False)
