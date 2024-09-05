
from rest_framework import serializers
from .models import cartModel,addToCart


class cartSerializer(serializers.ModelSerializer):

    class Meta:
        model=cartModel
        fields='__all__'

class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model=addToCart
        fields='__all__'
    

    