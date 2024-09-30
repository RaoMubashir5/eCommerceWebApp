from Cart.models import AddToCart
from UserApp.FrontEnd.views import get_user_name
from django.shortcuts import render
from django.shortcuts import redirect
from UserApp.models import *
import requests

def place_order(request,pk):
    token = request.session.get('access_token')
    if not token or not request.user.is_authenticated:
        return ('/api/home/')
    headers = {'Authorization': f"Bearer {token}"}
    requesting_response = requests.post(f"http://127.0.0.1:8000/api/addOrder/{pk}", headers = headers)
    if requesting_response.status_code != 201:
        if requesting_response.status_code == 401:
            return redirect('/api/home/')
        if requesting_response.status_code == 403:
            response_in_json = requesting_response.json().get('output')
            return render(request, 'your_Cart.html', {'empty': True, 'massage': response_in_json})
        return render(request, 'your_Cart.html', {'empty': True, 'massage': "Order not placed some errors there"})
    previous_cart_instances = AddToCart.objects.filter(cart = pk)
    reset_cart = previous_cart_instances.delete()
    response_in_json = requesting_response.json().get('output')
    return render(request, 'your_Cart.html', {'empty': True, 'massage': response_in_json})
 
def all_orders_history(request):
        token = request.session.get('access_token')
        if not token :
            return redirect('/api/home/')
        headers = {'Authorization': f"Bearer {token}"}
        requesting_response = requests.get(f"http://127.0.0.1:8000/api/order/", headers = headers)
        if requesting_response.status_code == 200:
            response_in_json = requesting_response.json()
            return render(request, 'orderHistory.html', {'orders': response_in_json})
        else: 
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
            return render(request, 'orderHistory.html', {'erorr': "There are no orders to show."})
        
def single_orders_history(request, pk = None):
    token = request.session.get('access_token')
    if not token :
        return redirect('/api/home/')
    headers = {'Authorization': f"Bearer {token}"}
    requesting_response = requests.get(f"http://127.0.0.1:8000/api/singleOrder/{pk}", headers = headers)
    if requesting_response.status_code != 200:
        if requesting_response.status_code == 401:
            return redirect('/api/home/')
        return render(request, 'orderedItems.html', {'massage': "No details available."})
    response_in_json = requesting_response.json()
    orders = response_in_json.get('Order_Details')
    user_who_ordered = get_user_name(orders.get('ordered_by_user'), headers)
    total_bill = orders.get('total_bill')
    items_details = response_in_json.get('Cart_items')
    context = { 
                'orders': user_who_ordered,
                'total_bill': total_bill,
                'Items_details': items_details,                   
              }
    return render(request, 'orderedItems.html', context)
                    


                
















        
        