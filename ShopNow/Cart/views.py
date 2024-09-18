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
                   

                


            



        
        