from rest_framework.views import APIView
from Cart.models import AddToCart
from ..customPermissions import CustomizeAPIPermissions
from UserApp.FrontEnd.views import get_user_name
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Order
from order.models import OrderItem
from ShopNow.allSerializers.orderSerializer import OrderSerializer
from ShopNow.allSerializers.orderSerializer import OrderItemSerializer
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from UserApp.models import *
from ..orderHistoryPermissions import OrderHistoryPermissions
import requests

class GetAllOrderApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request):
        order_history = Order.objects.all()
        if order_history:
            serialized_order = OrderSerializer(order_history, many = True)
            return Response(serialized_order.data, status = status.HTTP_200_OK)
        else:
            return Response({'response': "You hav'nt ordered yet!!"}, status = status.HTTP_400_BAD_REQUEST)
        
class GetOrderApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request, pk):
            try:
                order_history_instance = Order.objects.get(id = pk)
            except:
                return Response({"output": "There is no such Order with this order ID."}, status = status.HTTP_400_BAD_REQUEST)
            self.check_object_permissions(request, order_history_instance)       
            order_items = order_history_instance.items
            try:
                serialized_items = OrderItemSerializer(order_items, many = True)
            except:
                return Response("Issue with the Items serailizer", status = status.HTTP_204_NO_CONTENT) 
            serialized_order = OrderSerializer(order_history_instance)
            response_to_send = {'Cart_items': serialized_items.data, 'Order_Details': serialized_order.data}
            return Response(response_to_send, status = status.HTTP_200_OK)     

class AddOrderApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def post(self, request, pk):
            requesting_user = request.user
            request_dict = request.data
            cart_id = pk                          
            added_cart_obj = AddToCart.objects.filter(cart = cart_id)

            if not added_cart_obj.exists():
                return Response({'output': "Sorry!!, Your Cart is Empty!!"}, status = status.HTTP_403_FORBIDDEN)
            request_dict['ordered_by_user'] = requesting_user.id
            request_dict['total_bill'] = 0
            serialized = OrderSerializer(data = request_dict)

            if not serialized.is_valid():
                return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)
            order_instance = serialized.save()
            Total_bill = 0
            for cart in added_cart_obj:
                OrderItem.objects.create(order = order_instance, product = cart.cart_product,
                                        quantity = cart.product_quantity, price = cart.cart_product.price)
                Total_bill = Total_bill + (cart.cart_product.price * cart.product_quantity)

            order_instance.total_bill = Total_bill
            order_instance.save()  
            return Response({'output': "Your Order has been placed!!"}, status = status.HTTP_201_CREATED)
    
class UserOrders(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [OrderHistoryPermissions]

    def get(self, request, pk = None):
        if pk is None:
            order_history = Order.objects.all()
            if order_history:
                serialized = OrderSerializer(order_history, many = True)
                return Response(serialized.data,status=status.HTTP_200_OK) 
            return Response(f"There are no orders placed yet!!{pk}", status = status.HTTP_400_BAD_REQUEST)
        else:
            user_who_order = Webuser.objects.get(id = pk)
            self.check_object_permissions(request, user_who_order)
            order_history = user_who_order.user_orders.all()
            if order_history:
                serialized = OrderSerializer(order_history, many = True)
                return Response(serialized.data,status = status.HTTP_200_OK)
            return Response("You hav'nt ordered yet!!", status = status.HTTP_204_NO_CONTENT)
