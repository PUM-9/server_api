from django.http.response import HttpResponse
from api.models import Registration
import json

type_json = 'application/json'


def create_register_job(request):

    if request.method == 'GET':
        context = json.dumps({'status': 400, 'reason': 'Bad request'})
        response = HttpResponse(context, content_type=type_json)
        response.status_code = 400
        return response

    arguments = json.dumps(request.body.decode())
    job_created = Registration.create(arguments)
    if job_created:
        return HttpResponse('')
    else:
        context = json.dumps({'status': 406, 'reason': 'Job could not be created'})
        response = HttpResponse(context, content_type=type_json)
        response.status_code = 406
        return response
