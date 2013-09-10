from django.core.management.base import BaseCommand
from agent.models import Sighting, NormalizedSighting
from time import time
from math import floor

class Command(BaseCommand):
    args = ''
    help = 'Normalize and consolidate raw sighting data.'

    def handle(self, *args, **options):
        # start from the oldest unprocessed record
        ts = int(floor(time())) - 15
        sightings = Sighting.objects.filter(normalize_processed=False, timestamp__lte=ts).order_by('timestamp')
        while sightings.count() > 0:
            group = []
            try:
                # use the first record as the start of our set group
                first = sightings[0]
            except IndexError:
                return
            group.append(first)
            print("Processing %s - %s - %d" % (first.device_id, first.host, first.timestamp))

            # find more of this match in the same second
            more = sightings.filter(host=first.host, device_id=first.device_id, timestamp=first.timestamp)
            for sighting in more:
                group.append(sighting)
            
            # find more of this match in sequential seconds
            more = sightings.filter(host=first.host, device_id=first.device_id, timestamp=group[-1].timestamp + 1)
            while more.count() > 0:
                for sighting in more:
                    group.append(sighting)
                more = sightings.filter(host=first.host, device_id=first.device_id, timestamp=group[-1].timestamp + 1)

            # create the normalized sighting
            norm = NormalizedSighting(host=first.host, device_id=first.device_id, timestamp=first.timestamp)
            avg = []
            for sighting in group:
                if norm.signal_low is None or sighting.signal_dbm < norm.signal_low:
                    norm.signal_low = sighting.signal_dbm
                if norm.signal_high is None or sighting.signal_dbm > norm.signal_high:
                    norm.signal_high = sighting.signal_dbm
                avg.append(sighting.signal_dbm)
            norm.signal_avg = sum(avg) / len(avg)
            norm.num_samples = len(group) 
            norm.save()

            # record these sightings as normalized
            for sighting in group:
                sighting.normalize_processed = True
                sighting.save()
            sightings = Sighting.objects.filter(normalize_processed=False, timestamp__lte=ts).order_by('timestamp')
