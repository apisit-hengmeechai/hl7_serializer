from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from snippets.models import *
from snippets.serializers import *

import json
# Create your views here.
def index(request):
    return HttpResponse("<h1>Welcome</h1>")

@api_view(['GET'])
def patient_query(request, identifier_type, value, format=None):
    patient_set = Patient.objects.all()
    output = list(filter(lambda x: (len(x.identifier_set.filter(type=identifier_type.upper())) > 0) and (len(x.identifier_set.filter(value=str(value))) > 0), patient_set))
    p_set_ser = PatientSerializer(output, many=True)
    return HttpResponse(json.dumps(p_set_ser.data), content_type="application/json")

@api_view(['POST'])
def patient_add(request, format=None):
    data = json.loads(request.body)
    ser = PatientSerializer(data=data)
    valid = ser.is_valid()
    if valid:
        ser.save()
        return HttpResponse(json.dumps(ser.data), content_type="application/json")
    else:
        return HttpResponse(json.dumps(ser.errors), content_type="application/json", status=500)
    #patient_set = Patient.objects.all()
    #output = list(filter(lambda x: (len(x.identifier_set.filter(type=identifier_type.upper())) > 0) and (len(x.identifier_set.filter(value=str(value))) > 0), patient_set))
    #p_set_ser = PatientSerializer(output, many=True)
    