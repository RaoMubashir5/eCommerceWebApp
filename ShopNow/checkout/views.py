from rest_framework.response import Response
from .models import checkoutPage

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from rest_framework import status

from .serializer import checkoutSerializer
from .customPermissions import CustomizeAPIPermissions

from ShopNow.allSerializers.productSerializer import productSerializer
from Cart.models import addToCart
from ShopNow.allSerializers.cartSerializer import AddToCartSerializer


# Create your views here.0

class CheckoutView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]
    
    def post(self,request):
        if request.data:
            form_data=request.data
          
            requesting_user=request.user
            print("......",requesting_user)
          
            
            serialized=checkoutSerializer(data=form_data)

            if serialized.is_valid():
                serialized.save()
                cart_obj=requesting_user.Cart_with_this_user
            
                # using reverse relation we find the all addtocart entries with the cart of that user
                cart_against_this_user=cart_obj.products_inThisCart.all()
                serialized_products=AddToCartSerializer(cart_against_this_user,many=True)
                print(cart_against_this_user)

 
                cart_sum=0
                for cart_prod in cart_against_this_user:
                    print(cart_prod,cart_prod.cart_product,cart_prod.product_quantity)
                    cart_sum=cart_sum + (cart_prod.cart_product.price*cart_prod.product_quantity)

                print(cart_sum)
                #cart_sum= sum(prod.price*prod.add_product for prod in all_products_cart)
                response_to_beSend={'UserInfo':serialized.data,
                                    'cart_items':serialized_products.data,
                                    'Cart_sum':cart_sum,
                                    'button':"Proceed to Place order",
                                    }
                return Response(response_to_beSend,status=status.HTTP_201_CREATED)
            else:
                return Response(serialized.errors)
        return Response("Your request is empty",status=status.HTTP_400_BAD_REQUEST)
    
    
