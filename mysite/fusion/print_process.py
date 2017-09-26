# -*- coding: utf-8 -*-
import json, urllib2
import datetime
import time
from decimal import *
import logging
from demande.models import Task
from demande.models import states

# Get an instance of a logger
logger = logging.getLogger(__name__)


def make_print(task, modelename):
    '''
        Création de de la fusion
    '''

    # Info sur le modèle
    request_info = {
        "filename": "../" + modelename,
        "outputFilename": "RESULT_" + str(task.id) + ".docx",
        "runAsync": False,
    }

    # Définition des attributs du modèle
    data = {"date": task.date.strftime("%d-%m-%Y") if task.date != "" and task.date is not None else "",
                "obj": task.obj,
                "state": str(dict(states)[task.state])
            }

    if task.author is not None:    
        data["author"] = {
            "name": task.author.username,
            "email": task.author.email,
        }

    request_info['data'] = data

    #print json.dumps(request_info)

    # Appel du WS de fusion
    req = urllib2.Request("http://localhost:7000/rest/fusion/", data=json.dumps(request_info),
	                      headers={"Content-Type": "application/json"})
	
    response = urllib2.urlopen(req)
    url_response = response.read()
    response.close()

