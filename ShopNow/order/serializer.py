from rest_framework import serializers
from .models import order,orderItem

class orderSerializer(serializers.ModelSerializer):

    class Meta:
        model=order
        fields='__all__'

class orderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=orderItem
        fields='__all__'