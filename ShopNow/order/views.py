from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView

from .models import order,OrderItem

from order.serializer import orderSerializer,orderItemSerializer

from rest_framework import status

from rest_framework.response import Response
from UserApp.models import *

from checkout.serializer import checkoutSerializer
from checkout.models import checkoutPage
from Cart.models import cartModel,addToCart


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .customPermissions import CustomizeAPIPermissions

from .orderHistoryPermissions import orderHistoryPermissions

class orderApi(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]
    def get(self,request,pk=None):
        if pk is None:
            order_history=order.objects.all()
            if order_history:
                print("order history of ",order_history)
                # checkout_info_obj=
                # serialized_checkout_info=checkoutSerializer()
                serialized_order=orderSerializer(order_history,many=True)
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
        
            order_items=order_history_instance.items
            

            serialized_items=orderItemSerializer(order_items)
            serialized_order=orderSerializer(order_history_instance)

            response_to_send={'Cart_items':serialized_items.data,'Order-Details':serialized_order.data, }
            return Response(response_to_send,status=status.HTTP_200_OK)               
            
                 
                  
       # return Response("your request is empty.",status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,pk):
        #if request.data:
            requesting_user=request.user

            request_dict=request.data
            print("yahantak ok ha",request_dict)
            cart_id=pk #Cart id
            
            print("0222 yahan tak ok ha",cart_id,type(cart_id),cart_id)
                          
            added_cart_obj=addToCart.objects.filter(cart=cart_id)
          
            #adding the param data into the request.data
            request_dict['ordered_by_user']=requesting_user.id
            request_dict['total_bill']=50
            print("03 yahantak ok ha",request_dict)
            serialized=orderSerializer(data=request_dict)
            print("044 yahantak ok ha",request_dict)
            if serialized.is_valid():
                print(serialized.errors)
                order_instance=serialized.save()
                Total_bill=0
                for cart in added_cart_obj:
                    OrderItem.objects.create(order=order_instance,product=cart.cart_product,quantity=cart.product_quantity,
                                             price=cart.cart_product.price)
                    Total_bill=Total_bill+(cart.cart_product.price * cart.product_quantity)
                order_instance.total_bill=Total_bill
                order_instance.save()  
                return Response("Your Order has been placed!!",status=status.HTTP_400_BAD_REQUEST)
            else:
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





