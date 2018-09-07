import datetime
import os
import re
import time

from .models import *
from rest_framework import serializers

class Script(serializers.Serializer):
    pn = serializers.CharField(max_length=200)
    rn = serializers.IntegerField(max_value=None, min_value=1)
    resd = serializers.CharField(max_length=200)
    cutoff = serializers.FloatField(max_value=None, min_value=None)
    file = serializers.FileField(max_length=None, allow_empty_file=False, use_url=True)

    def validate_file(self, value):
        if not value.name.endswith('.zip'):
            if not value.name.endswith('.ZIP'):
                raise serializers.ValidationError("Invalid File")
        return value