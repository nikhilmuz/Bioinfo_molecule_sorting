# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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

class Run(APIView):
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
            return Response(
                open(os.getcwd() + '/uploads/' + folder+".zip", "r"),
                status=status.HTTP_201_CREATED,
                content_type='application/zip'
            )
        else:
            return Response(script_serializer.errors, status=status.HTTP_400_BAD_REQUEST)