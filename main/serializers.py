from rest_framework import serializers
from .models import *


class NeedySerializer(serializers.ModelSerializer):
    class Meta:
        model = Needy
        fields = '__all__'

