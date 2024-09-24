from .models import AddToCart
from rest_framework.views import APIView
from ShopNow.allSerializers.cartSerializer import AddToCartSerializer
from ShopNow.allSerializers.cartSerializer import CartSerializer
from .customPermissions import CustomizeAPIPermissions
from .models import CartModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from product.models import *
import requests

class AddcartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request):
        if request.user:
            owner_cart_user = request.user
            cartobj = CartModel.objects.get(user_of_cart = owner_cart_user)
            if cartobj:
                all_cart_items = cartobj.products_inThisCart.all()
                if all_cart_items.exists():
                    serialized = AddToCartSerializer(all_cart_items, many = True)
                    return Response(serialized.data, status = status.HTTP_200_OK)
                return Response("you have nothing in your Cart", status = status.HTTP_204_NO_CONTENT)
            else:
                return Response("your Cart is not exists", status = status.HTTP_204_NO_CONTENT)
        else:
            return Response("User is no received!!")        
        
    def post(self,request):
        cart_product_id = request.data.get('cart_product')
        cart_id = request.data.get('cart')
        product_quantity = request.data.get('product_quantity', 1)
        cart = CartModel.objects.get(id = cart_id)
        product = AddToCart.objects.filter(cart = cart, cart_product = cart_product_id).first()
        if product:
                product.product_quantity += 1
                product.save()
                serialized = AddToCartSerializer(product)
                return Response(serialized.data, status = status.HTTP_200_OK)                
        else:
            serialized = AddToCartSerializer(data = request.data, many = False)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response({"Errors": f"Request data is not valid, {serialized.errors} ."}, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, product_id):
            owner_cart_user = request.user
            cartobj = CartModel.objects.get(user_of_cart = owner_cart_user)
            if cartobj and product_id is  not None:
                all_cart_items = cartobj.products_inThisCart.all()
                try:
                    if all_cart_items.get(cart_product = product_id):
                        instance = cartobj.products_inThisCart.get(cart_product = product_id)
                    else:
                        return Response("this product is not in Cart")
                    self.check_object_permissions(request, instance)
                    instance.delete()
                    return Response("Deleted successfully!!", status = status.HTTP_200_OK)     
                except:
                       return Response("Product is not in the Cart!!",status = status.HTTP_204_NO_CONTENT)                   
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST) 
                   
def add_to_cart_frontend(request, pk):
    token = request.session.get('access_token')
    if token:
        headers = {'Authorization': f"Bearer {token}"}
        check = request.user.is_authenticated
        user_id = request.session.get('user_id')
        product_quantity = request.GET.get('quantity',1)
        user_cart = CartModel.objects.get(user_of_cart = user_id)
        data={
                'cart_product': pk,
                'cart': user_cart.id,
                'product_quantity': product_quantity,
            }
        requesting_response = requests.post("http://127.0.0.1:8000/api/addToCart/", data = data, headers = headers)
        response_api = requesting_response.json()
        if requesting_response.status_code == 201 or requesting_response.status_code == 200:
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
        requesting_response = requests.get("http://127.0.0.1:8000/api/addToCart/", headers = headers)
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
        requesting_response = requests.delete(f"http://127.0.0.1:8000/api/addToCart/{product_id}", headers = headers)
        
        if requesting_response.status_code == 200:
            response_in_json = requesting_response.json()
            requesting_response = requests.get("http://127.0.0.1:8000/api/addToCart/", headers = headers)
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
            



        
        