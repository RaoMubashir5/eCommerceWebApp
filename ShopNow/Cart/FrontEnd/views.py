from Cart.models import CartModel
from django.shortcuts import render
from django.shortcuts import redirect
from product.models import *
import requests

def add_to_cart_frontend(request, pk):
    token = request.session.get('access_token')
    if token:
        headers = {'Authorization': f"Bearer {token}"}
        check = request.user.is_authenticated
        user_id = request.session.get('user_id')
        product_quantity = request.GET.get('quantity',1)
        data = {
                'cart_product': pk,
                'product_quantity': product_quantity,
            }
        requesting_response = requests.post("http://127.0.0.1:8000/api/addToCart/", data = data, headers = headers)
        if requesting_response.status_code == 201 or requesting_response.status_code == 200:
            response_api = requesting_response.json()
            return redirect('/api/showCart/')
        else:
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
            else:
                print(response_api)
                return redirect('/api/home/')
    else:
        if requesting_response.status_code == 401:
            return redirect('/api/home/')
            
def show_cart(request):
    token = request.session.get('access_token')
    if token and request.user.is_authenticated:
        headers = {'Authorization': f"Bearer {token}"}
        requesting_response = requests.get("http://127.0.0.1:8000/api/getCart/", headers = headers)
        if requesting_response.status_code == 200:
            response_in_json = requesting_response.json()
            product_info = []
            for each_cart in response_in_json:
                product_obj = Product.objects.get(id = each_cart.get('cart_product'))
                product_info.append({'product_obj': product_obj, 'quantity': each_cart.get('product_quantity'),
                                     'cart': each_cart.get('cart')})
                cart_id = each_cart.get('cart')
            return render(request, 'your_Cart.html', {'empty': False, 'product_info': product_info, 'cart_id': cart_id})
        else:
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
            if requesting_response.status_code == 204:
                return render(request, 'your_Cart.html', {'empty': True, 'massage': "Your Cart is Empty!!"})

def delete_prod_from_cart(request, product_id):
    token = request.session.get('access_token')
    if token and request.user.is_authenticated:
        headers = {'Authorization': f"Bearer {token}"}
        requesting_response = requests.delete(f"http://127.0.0.1:8000/api/deleteCart/{product_id}", headers = headers)
        
        if requesting_response.status_code == 200:
            response_in_json = requesting_response.json()
            requesting_response = requests.get("http://127.0.0.1:8000/api/getCart/", headers = headers)
            if requesting_response.status_code == 200:
                response_in_json = requesting_response.json()
                product_info = []
                for each_cart in response_in_json:
                    product_obj = Product.objects.get(id = each_cart.get('cart_product'))
                    product_info.append(
                                        {
                                          'product_obj': product_obj,
                                          'quantity': each_cart.get('product_quantity'),
                                          'cart': each_cart.get('cart')
                                        }
                                    )
                    cart_id = each_cart.get('cart')
                return render(
                               request,
                               'your_Cart.html',
                               {
                                'empty': False,
                                'product_info': product_info,
                                'cart_id': cart_id,
                                'delete_massage': "deleted successfully"
                               }
                            )
            else:
                if requesting_response.status_code == 401:
                    return redirect('/api/home/')
                if requesting_response.status_code == 204:
                    return render(request,
                                 'your_Cart.html',
                                 {'empty': True,
                                  'massage': "Your Cart is Empty!!"
                                 }
                                )
                return render(request,
                              'your_Cart.html',
                              {'empty':False,
                               'product_info':product_info,
                               'cart_id':cart_id
                              }
                            )
        else:
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
            



        
        