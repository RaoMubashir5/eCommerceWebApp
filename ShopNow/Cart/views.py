from django.shortcuts import render,redirect

from rest_framework.response import Response

from rest_framework.views import APIView
from .serializer import cartSerializer,AddToCartSerializer
from rest_framework import status
from .models import addToCart,cartModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from .customPermissions import CustomizeAPIPermissions
import requests
from product.models import *
# Create your views here.


class AddcartView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]
    def get(self,request):

        if request.user:
            owner_cart_user=request.user
            cartobj=cartModel.objects.get(user_of_cart=owner_cart_user)
            if cartobj:
                all_cart_items=cartobj.products_inThisCart.all()
                print("$$$$",all_cart_items,"$$$$")
                if all_cart_items.exists():
                    serialized=AddToCartSerializer(all_cart_items,many=True)
                    print("ok request")
                    return Response(serialized.data,status=status.HTTP_200_OK)
                return Response("you have nothing in your Cart",status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("your Cart is not exists",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("User is no received!!")        
        
            
    def post(self,request):
         # Parse the request data
        cart_product_id = request.data.get('cart_product')
        cart_id = request.data.get('cart')
        product_quantity = request.data.get('product_quantity', 1)

        # Fetch the cart and product

        cart = cartModel.objects.get(id=cart_id)
        product = addToCart.objects.filter(cart=cart, cart_product=cart_product_id).first()

        if product:
                # Increment quantity if product already in the cart
                product.product_quantity += 1
                product.save()
                serialized = AddToCartSerializer(product)
                return Response(serialized.data, status=status.HTTP_200_OK)                
        else:
            serialized = AddToCartSerializer(data=request.data,many=False)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data,status=status.HTTP_201_CREATED)

            else:
                print(f"Validation errors: {serialized.errors}")
                return Response({"Errors": f"Request data is not valid, {serialized.errors} ."},status=status.HTTP_400_BAD_REQUEST)
 
    
    def delete(self,request,product_id):
        #product name would be send as query param  
            owner_cart_user=request.user
            print("%%%",owner_cart_user,product_id,product_id)
            cartobj=cartModel.objects.get(user_of_cart=owner_cart_user)
            print("<,,,>",owner_cart_user,cartobj)
            if cartobj and product_id is  not None:
                all_cart_items=cartobj.products_inThisCart.all()
                try:
                    if all_cart_items.get(cart_product=product_id):
                        instance=cartobj.products_inThisCart.get(cart_product=product_id)
                    else:
                        return Response("this product is not in Cart")
                
                    self.check_object_permissions(request,instance)
                    instance.delete()
                    return Response("Deleted successfully!!",status=status.HTTP_200_OK)     
                except:
                       print()
                       return Response("Product is not in the Cart!!")                   
               
            else:
                print("Cart object or product tobe deleted not sent!!")
                   


def AddToCart(request,pk):
    token=request.session.get('access_token')
    if token:
        headers={'Authorization': f"Bearer {token}"}

            #decoding the token to extract the userr id :
            #decode_token=JWT
        check=request.user.is_authenticated

        print("User status: ",check,"token is ",token,".....")
        user_id=request.session.get('user_id')
        product_quantity=request.GET.get('quantity',1)
        user_cart=cartModel.objects.get(user_of_cart=user_id)
  
        data={
                'cart_product':pk,
                'cart':user_cart.id,
                'product_quantity':product_quantity,
            }
                  
        requesting_response=requests.post("http://127.0.0.1:8000/api/addToCart/",data=data,headers=headers)
     
        response_api=requesting_response.json()
        print("envrnvkrvnrev:::",response_api)
        if requesting_response.status_code==201 or requesting_response.status_code==200:
            return redirect('/api/showCart/')
        else:
            if requesting_response.status_code==401:
                return redirect('/api/home/')
            else:
                print(response_api)
                return redirect('/api/home/')

    else:
        if requesting_response.status_code==401:
            return redirect('/api/home/')
            


def showCart(request):
    token=request.session.get('access_token')
    if token and request.user.is_authenticated:
        headers={'Authorization': f"Bearer {token}"}
        requesting_response=requests.get("http://127.0.0.1:8000/api/addToCart/",headers=headers)

        if requesting_response.status_code==200:
            response_in_json=requesting_response.json()
            product_info = []

            for each_cart in response_in_json:
                print("Each Cart Item:", each_cart)
                product_obj=product.objects.get(id=each_cart.get('cart_product'))
                product_info.append({'product_obj':product_obj,'quantity':each_cart.get('product_quantity'),
                                     'cart':each_cart.get('cart')})
                cart_id=each_cart.get('cart')
            return render(request,'your_Cart.html',{'empty':False,'product_info':product_info,'cart_id':cart_id})
        
        else:
            if requesting_response.status_code==401:
                return redirect('/api/home/')
            if requesting_response.status_code==204:
                return render(request,'your_Cart.html',{'empty':True,'massage':"Your Cart is Empty!!"})


def deleteProdFromCart(request,product_id):
    token=request.session.get('access_token')
    if token and request.user.is_authenticated:
        headers={'Authorization': f"Bearer {token}"}
        requesting_response=requests.delete(f"http://127.0.0.1:8000/api/addToCart/{product_id}",headers=headers)
        
        if requesting_response.status_code==200:
            response_in_json=requesting_response.json()
            print("Deleted: ",response_in_json)
            requesting_response=requests.get("http://127.0.0.1:8000/api/addToCart/",headers=headers)

            if requesting_response.status_code==200:
                response_in_json=requesting_response.json()
                product_info = []

                for each_cart in response_in_json:
                    print("Each Cart Item:", each_cart)
                    product_obj=product.objects.get(id=each_cart.get('cart_product'))
                    product_info.append({'product_obj':product_obj,'quantity':each_cart.get('product_quantity'),
                                        'cart':each_cart.get('cart')})
                    cart_id=each_cart.get('cart')
                return render(request,'your_Cart.html',{'empty':False,'product_info':product_info,'cart_id':cart_id,
                                                        'delete_massage':"deleted successfully"})
            
            else:
                if requesting_response.status_code==401:
                    return redirect('/api/home/')
                if requesting_response.status_code==204:
                    return render(request,'your_Cart.html',{'empty':True,'massage':"Your Cart is Empty!!"})
                return render(request,'your_Cart.html',{'empty':False,'product_info':product_info,'cart_id':cart_id})
        else:
            if requesting_response.status_code==401:
                return redirect('/api/home/')
            # else:
            #     return render(request,'your_Cart.html',{'empty':True,'massage':"Cannot delete!!"})

            



        
        