from ..models import AddToCart
from rest_framework.views import APIView
from ShopNow.allSerializers.cartSerializer import AddToCartSerializer
from Cart.customPermissions import CustomizeAPIPermissions
from Cart.models import CartModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from product.models import *


class GetCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request):
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
    
class AddCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def post(self, request):
        data = request.data.copy()
        cart_product_id = request.data.get('cart_product')
        cart_id = request.user.Cart_with_this_user
        product_quantity = request.data.get('product_quantity', 1)
        cart = CartModel.objects.get(id = cart_id.id)
        data['cart'] =  cart.id
        print(data)
        product = AddToCart.objects.filter(cart = cart, cart_product = cart_product_id).first()
        if not product:
            serialized = AddToCartSerializer(data = data, many = False)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response({"Errors": f"Request data is not valid, {serialized.errors} ."}, status = status.HTTP_400_BAD_REQUEST)
        product.product_quantity += 1
        product.save()
        serialized = AddToCartSerializer(product)
        return Response(serialized.data, status = status.HTTP_200_OK)                

class DeleteCartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

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
 