import rest_framework
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer #it is to convert the python dictionry into json as in api only json reponse will be sent.
from product.models import product

class productSerializer(serializers.ModelSerializer):

    class Meta:
        model=product
        fields='__all__'
    



