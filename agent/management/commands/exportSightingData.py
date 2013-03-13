from django.core.management.base import BaseCommand, CommandError
from agent.models import Sighting
import csv


class Command(BaseCommand):
    args = ''
    help = 'Export and process sighting data'

    def handle(self, *args, **options):
        file = open('/tmp/sightingData.csv', 'w')
        writer = csv.writer(file, delimeter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        pingCount = 0
        dbmTotal = 0
        previousDeviceId = ''
        timeTotal = 0

        for sighting in Sighting.objects.all():
            if sighting.device_id == previousDeviceId:
                pingCount = pingCount + 1
                dbmTotal += sighting.signal_dbm
                timeTotal += sighting.timestamp
            else:
                writer.writerow([previousDeviceId, pingCount, dbmTotal / pingCount, timeTotal / pingCount])
                pingCount = 0
                dbmTotal = sighting.signal_dbm
                timeTotal = sighting.timestamp

            previousDeviceId = sighting.device_id
