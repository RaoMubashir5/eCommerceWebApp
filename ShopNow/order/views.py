from rest_framework.views import APIView
from Cart.models import AddToCart
from .customPermissions import CustomizeAPIPermissions
from UserApp.FrontEnd.views import get_user_name
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order
from .models import OrderItem
from ShopNow.allSerializers.orderSerializer import OrderSerializer
from ShopNow.allSerializers.orderSerializer import OrderItemSerializer
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from UserApp.models import *
from .orderHistoryPermissions import OrderHistoryPermissions
import requests

class OrderApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request, pk = None):
        if pk is None:
            order_history = Order.objects.all()
            if order_history:
                serialized_order = OrderSerializer(order_history, many = True)
                return Response(serialized_order.data, status = status.HTTP_200_OK)
            else:
                return Response({'response': "You hav'nt ordered yet!!"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            try:
                order_history_instance = Order.objects.get(id = pk)
            except:
                return Response("There is no such Order with this order ID.", status = status.HTTP_400_BAD_REQUEST)
            self.check_object_permissions(request, order_history_instance)       
            order_items = order_history_instance.items
            try:
                serialized_items = OrderItemSerializer(order_items, many = True)
            except:
                return Response("Issue witht the Items serailizer", status = status.HTTP_204_NO_CONTENT) 
            serialized_order = OrderSerializer(order_history_instance)
            response_to_send = {'Cart_items': serialized_items.data, 'Order_Details': serialized_order.data}
            return Response(response_to_send, status = status.HTTP_200_OK)     
    
    def post(self, request, pk):
            requesting_user = request.user
            request_dict = request.data
            cart_id = pk                          
            added_cart_obj = AddToCart.objects.filter(cart = cart_id)
            request_dict['ordered_by_user'] = requesting_user.id
            request_dict['total_bill'] = 50
            serialized = OrderSerializer(data = request_dict)
            if serialized.is_valid():
                order_instance = serialized.save()
                Total_bill = 0
                for cart in added_cart_obj:
                    OrderItem.objects.create(order = order_instance, product = cart.cart_product,
                                             quantity = cart.product_quantity, price = cart.cart_product.price)
                    Total_bill = Total_bill + (cart.cart_product.price * cart.product_quantity)
                order_instance.total_bill = Total_bill
                order_instance.save()  
                return Response("Your Order has been placed!!", status = status.HTTP_201_CREATED)
            else:
                return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
    
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

def place_order(request,pk):
    token = request.session.get('access_token')
    if token and request.user.is_authenticated:
        headers = {'Authorization': f"Bearer {token}"}
        requesting_response = requests.post(f"http://127.0.0.1:8000/api/order/{pk}", headers = headers)
        if requesting_response.status_code == 201:
            cart_instances = AddToCart.objects.filter(cart = pk)
            reset_cart = cart_instances.delete()
            response_in_json = requesting_response.json()
            product_info = []
            return render(request, 'your_Cart.html', {'empty': True, 'product_info': product_info, 'massage': response_in_json})
        else:
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
            return render(request, 'your_Cart.html', {'empty': True, 'massage': "Order not placed some errors there"})
 
def orders_history(request, pk = None):
        token = request.session.get('access_token')
        if token :
            headers = {'Authorization': f"Bearer {token}"}
            if pk is None:
                requesting_response = requests.get(f"http://127.0.0.1:8000/api/order/", headers = headers)
                if requesting_response.status_code == 200:
                    response_in_json = requesting_response.json()
                    return render(request, 'orderHistory.html', {'orders': response_in_json})
                else: 
                    if requesting_response.status_code == 401:
                        return redirect('/api/home/')
                    return render(request, 'orderHistory.html', {'erorr': "There are no orders to show."})
            else:
                requesting_response = requests.get(f"http://127.0.0.1:8000/api/order/{pk}", headers = headers)
                if requesting_response.status_code == 200:
                    response_in_json = requesting_response.json()
                    orders = response_in_json.get('Order_Details')
                    user_who_ordered = get_user_name(orders.get('ordered_by_user'), headers)
                    total_bill = orders.get('total_bill')
                    return render(request, 'orderedItems.html', {'orders': user_who_ordered, 'total_bill': total_bill,
                                                               'Items_details': response_in_json.get('Cart_items')})
                else: 
                    if requesting_response.status_code == 401:
                        return redirect('/api/home/')
                    return render(request, 'orderedItems.html', {'massage': "No details available."})
        else:
            return redirect('/api/home/')

                
















        
        