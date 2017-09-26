# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Task

# Create your views here.

def loadAjax(request):
    state = request.GET["state"]
    periode = request.GET["periode"]

    date_start = ""
    date_end = ""
    if periode != "":
        # Modification du format de la periode pour etre lisible
        periode = periode.replace(" ", "");
        periode = periode.replace("-", ",");
        periode = periode.replace("/", "-");

        date_start = periode.split(",")[0]
        date_end = periode.split(",")[1]

    if state == "1": #Todo        
        if date_start != "" and date_end != "":
            resultset = Task.objects.filter(state=state)\
            .filter(date__range=[date_start, date_end])\
            .order_by('date')[:50]
        else:
            resultset = Task.objects.filter(state=state)\
            .order_by('date')[:50]
    
    if state == "2": #Done
        if date_start != "" and date_end != "":
            resultset = Task.objects.filter(state=state)\
            .filter(date__range=[date_start, date_end])\
            .order_by('date')[:50]
        else:
            resultset = Task.objects.filter(state=state)\
            .order_by('date')[:50]
        

    results = [ob.as_json() for ob in resultset]
    response = json.dumps(results, indent=4)

    return HttpResponse(response, content_type="application/json")