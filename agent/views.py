from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from agent.models import Sighting


@csrf_exempt
def report(request):
    if (request.method == 'POST'
      and request.POST.get('host') is not None
      and request.POST.get('device_id') is not None
      and request.POST.get('timestamp') is not None
      and request.POST.get('signal_dbm') is not None):

        # create a new sighting from the request
        Sighting.objects.create(
            host=request.POST.get('host'),
            device_id=request.POST.get('device_id'),
            timestamp=request.POST.get('timestamp'),
            signal_dbm=request.POST.get('signal_dbm'))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
