from django.shortcuts import render,redirect

from rest_framework.response import Response

from rest_framework.views import APIView
from .serializer import cartSerializer,AddToCartSerializer
from rest_framework import status
from .models import addToCart,cartModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from .customPermissions import CustomizeAPIPermissions
import requests
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
                if all_cart_items.exists():
                    serialized=AddToCartSerializer(all_cart_items,many=True)
                    return Response(serialized.data)
                return Response("you have nothing in your Cart")
            else:
                return Response("your Cart is not exists")
        else:
            return Response("User is no received!!")        
        
            
    def post(self,request):
        if request.data:
            serialized=AddToCartSerializer(data=request.data)
            #product=serialized.data.get('cart_product')
            print("Product added in cart: ")
            if serialized.is_valid():
                try:
                    serialized.save()
                except:
                    return Response(f"Its already saved, {serialized.errors} .")
                return Response(serialized.data,status=status.HTTP_201_CREATED)
            else:
                return Response(f"Cart data is not valid {serialized.errors}",status=status.HTTP_400_BAD_REQUEST)
        return Response("Cart Request is Empty",status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        #product name would be send as query param  
        if request.data:
            owner_cart_user=request.user
            cartobj=cartModel.objects.get(user_of_cart=owner_cart_user)
            if cartobj and request.data.get('cart_product'):
                all_cart_items=cartobj.products_inThisCart.all()
                try:
                    if all_cart_items.get(cart_product=request.data.get('cart_product')):
                        instance=cartobj.products_inThisCart.get(cart_product=request.data.get('cart_product'))
                    else:
                        return Response("this product is not in Cart")
                
                    self.check_object_permissions(request,instance)
                    instance.delete()
                    return Response("Deleted successfully!!")     
                except:
                       return Response("Product is not in the Cart!!")                   
               
            else:
                print("Cart object or product tobe deleted not sent!!")
                   


def AddToCart(request,pk):
    token=request.session.get('access_token')
    if token:
        headers={'Authorization': f"Bearer {token}"}
            #decoding the token to extract the userr id :
            #decode_token=JWT
        print("............",headers)
        #requesting_response=requests.get(f"http://127.0.0.1:8000/api/product/{pk}",headers=headers)
        response_in_json=requesting_response.json()
        data={
            'cart_product':pk,''
        }
        requesting_response=requests.post(f"http://127.0.0.1:8000/api/addToCart/",headers=headers)
        response_in_json=requesting_response.json()
        print(";;;;;;;;;;;;;",response_in_json)
        if requesting_response.status_code==200:
            return render(request,'products_list.html',{'products':response_in_json})
        else:
            if requesting_response.status_code==401:
                return redirect('/api/home/')






        
        