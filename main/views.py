# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from wsgiref.util import FileWrapper

from django.views.generic.base import View

from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .VS_Script import *
import datetime
import time
import subprocess
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
from rest_framework.renderers import BaseRenderer

class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/zip'
    format = None
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

class Run(APIView):
    renderer_classes = (BinaryFileRenderer,)
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        script_serializer = Script(data=request.data)
        if script_serializer.is_valid():
            folder = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))
            path = os.getcwd() + '/uploads/' + folder + '/'
            data = request.FILES['file']
            default_storage.save(path+"a.zip", ContentFile(data.read()))
            subprocess.call("unzip "+path+"a.zip -d "+path, shell=True)
            screen(
                path,
                request.POST['pn'],
                request.POST['rn'],
                json.loads(request.POST['resd']),
                request.POST['cutoff'],
            )
            subprocess.call("zip -r "+os.getcwd() + '/uploads/' + folder+".zip "+path+"Best_molecules/*", shell=True)
            subprocess.call("rm -rf "+path, shell=True)
            data = open(os.getcwd() + '/uploads/' + folder+".zip", "rb").read()
            subprocess.call("rm " + os.getcwd() + '/uploads/' + folder + ".zip", shell=True)
            return Response(
                data,
                status=status.HTTP_201_CREATED,
                headers={'Content-Disposition': 'attachment', 'filename': 'result.pdf'},
                content_type='application/zip'
            )
        else:
            return Response(script_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ui.html', context=None, content_type=None, status=None, using=None)