from rest_framework import serializers
from order.models import order,OrderItem

class orderSerializer(serializers.ModelSerializer):

    class Meta:
        model=order
        fields='__all__'

class orderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderItem
        fields='__all__'