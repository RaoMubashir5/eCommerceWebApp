from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView

from .models import order

from order.serializer import orderSerializer

from rest_framework import status

from rest_framework.response import Response

from checkout.serializer import checkoutSerializer
from checkout.models import checkoutPage

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .customPermissions import CustomizeAPIPermissions

class orderApi(APIView):
    authentication_classes=['JWTAuthentication']
    permission_classes=['CustomizeAPIPermissions']
    def get(self,request):
        if request.data:
            requesting_user=request.user
            order_history=requesting_user.user_orders.all()
            checkout_info_obj=order_history.checkout_info
            serialized_checkout_info=checkoutSerializer(checkout_info_obj)
            serialized_order=orderSerializer(order_history,many=True)
            response_to_send={'serialized_checkout_info':serialized_checkout_info,
                            'serialized_order':serialized_order, }
            return Response(response_to_send,status=status.HTTP_200_OK)
        return Response("your request is empty.",status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        if request.data:
            requesting_user=request.user
            request_dict=request.data
            checkout_id=request.get('checkout_page_id') #pass param
            bill=request.get('total_bill')#pass in query param
            checkout_obj=checkoutPage.objects.get(id=int(checkout_id))
            #adding the param data into the request.data
            request_dict['user_ordering']=requesting_user
            request_dict['checkout_info']=checkout_obj
            request_dict['total_bill']=bill

            serialized=orderSerializer(data=request_dict)
            if serialized.is_valid():
                return Response("Your Order has been placed!!",status=status.HTTP_201_CREATED)
        return Response("your request is empty.",status=status.HTTP_400_BAD_REQUEST)

        





