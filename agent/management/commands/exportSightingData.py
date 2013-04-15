from django.core.management.base import BaseCommand, CommandError
from agent.models import Sighting
import csv


class Command(BaseCommand):
    args = ''
    help = 'Export and process sighting data'

    def handle(self, *args, **options):
        file = open('/tmp/sightingData.csv', 'w')
        writer = csv.writer(file)
        pingCount = 0
        dbmTotal = 0
        previousDeviceId = ''
        timeTotal = 0

        for sighting in Sighting.objects.all():
            # self.stdout.write(sighting.device_id + " | " + str(sighting.timestamp) + "\n")
            if sighting.device_id == previousDeviceId or previousDeviceId == '':
                pingCount += 1
                dbmTotal += sighting.signal_dbm
                timeTotal += sighting.timestamp
            else:
                writer.writerow([previousDeviceId, pingCount, dbmTotal / pingCount, timeTotal / pingCount])
                pingCount = 1
                dbmTotal = sighting.signal_dbm
                timeTotal = sighting.timestamp

            previousDeviceId = sighting.device_id
