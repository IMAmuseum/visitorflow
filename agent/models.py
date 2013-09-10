from django.db import models


class Sighting(models.Model):
    host = models.CharField(max_length=32)
    device_id = models.CharField(max_length=32)
    signal_dbm = models.IntegerField()
    timestamp = models.IntegerField(db_index=True)
    normalize_processed = models.BooleanField(default=False)


class NormalizedSighting(models.Model):
	host = models.CharField(max_length=32)
	device_id = models.CharField(max_length=32)
	signal_low = models.IntegerField()
	signal_high = models.IntegerField()
	signal_avg = models.IntegerField()
	num_samples = models.IntegerField()
	timestamp = models.IntegerField()
