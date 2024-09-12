from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView

from .models import order

from order.serializer import orderSerializer

from rest_framework import status

from rest_framework.response import Response
from UserApp.models import *

from checkout.serializer import checkoutSerializer
from checkout.models import checkoutPage
from Cart.serializer import cartSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .customPermissions import CustomizeAPIPermissions

from .orderHistoryPermissions import orderHistoryPermissions

class orderApi(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]
    def get(self,request,pk=None):
        if pk is None:
            requesting_user=request.user
            order_history=requesting_user.user_orders.all()
            if order_history:
                print("order history of ",requesting_user," :",order_history)
                # checkout_info_obj=
                # serialized_checkout_info=checkoutSerializer()
                serialized_order=orderSerializer(order_history,many=True)
                print(serialized_order)
                # response_to_send={'serialized_checkout_info':serialized_checkout_info,
               
                return Response(serialized_order.data,status=status.HTTP_200_OK)
            else:
                print("No............Orders")
                return Response({'response':"You hav'nt ordered yet!!"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                order_history_instance=order.objects.get(id=pk)
            except:
                return Response("There isno such Order with this order ID.",status=status.HTTP_400_BAD_REQUEST)
            self.check_object_permissions(request,order_history_instance)
                # user_Who_ordered=order_history_instance.ordered_by_user

            checkout_info_obj=order_history_instance.checkout_info
            serialized_checkout_info=checkoutSerializer(checkout_info_obj)

            serialized_order=orderSerializer(order_history_instance)

            response_to_send={'Checkout-User-Info':serialized_checkout_info.data,'Order-Details':serialized_order.data, }
            return Response(response_to_send,status=status.HTTP_200_OK)               
            
                 
                  
       # return Response("your request is empty.",status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        #if request.data:
            requesting_user=request.user
            request_dict=request.data
            print("yahantak ok ha",request_dict)
            checkout_id=request.query_params.get('checkout_page_id') #pass param
            bill=request.query_params.get('total_bill')#pass in query param
            print("0222 yahan tak ok ha",checkout_id,type(checkout_id),checkout_id)
                          
            checkout_obj=checkoutPage.objects.get(id=checkout_id)
            #adding the param data into the request.data
            request_dict['ordered_by_user']=requesting_user.id
            request_dict['checkout_info']=checkout_obj.id
            request_dict['total_bill']=bill
            print("03 yahantak ok ha",request_dict)
            serialized=orderSerializer(data=request_dict)
            print("044 yahantak ok ha",request_dict)
            if serialized.is_valid():
                print(serialized.errors)
                serialized.save()
                return Response("Your Order has been placed!!",status=status.HTTP_400_BAD_REQUEST)
            print("Errors")
            return Response(serialized.errors,status=status.HTTP_201_CREATED)
                  
        #return Response("your request is empty.",status=status.HTTP_400_BAD_REQUEST)

        


class userOrders(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[orderHistoryPermissions]
    def get(self,request,pk=None):
       
        if pk is None:
            order_history=order.objects.all()
            if order_history:
                serialized=orderSerializer(order_history,many=True)
                if serialized.is_valid():
                    serialized.save()
                    return Response(serialized.data,status=status.HTTP_200_OK)
                return Response(f"Invlaid orders data{pk}",status=status.HTTP_400_BAD_REQUEST)
            return Response(f"There are no orders placed yet!!{pk}",status=status.HTTP_400_BAD_REQUEST)
        else:
            user_who_order=Webuser.objects.get(id=pk)
            print("user_who_order :",user_who_order)
            self.check_object_permissions(request,user_who_order)
            order_history=user_who_order.user_orders.all()
            if order_history:
                serialized=orderSerializer(order_history,many=True)
                return Response(serialized.data,status=status.HTTP_200_OK)
                
            return Response("You hav'nt ordered yet!!",status=status.HTTP_400_BAD_REQUEST)





