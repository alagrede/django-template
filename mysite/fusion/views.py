# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import os
#import mimetypes
#mimetypes.init()

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def __getdoc__(filename):
    '''
        Stream du document
    '''
    wrapper = FileWrapper(file(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filename)
    response['Content-Length'] = os.path.getsize(filename)

    return response
