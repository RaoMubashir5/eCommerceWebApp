from rest_framework.response import Response
from .models import checkoutPage

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from rest_framework import status

from .serializer import checkoutSerializer
from .customPermissions import CustomizeAPIPermissions

from product.serializer import productSerializer


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
                all_products_cart=cart_obj.cart_product.all()
                serialized_products=productSerializer(all_products_cart,many=True)
                print(all_products_cart)
                response_to_beSend={'UserInfo':serialized.data,
                                    'cart_items':serialized_products.data,
                                    'button':"Proceed to Place order",}
                return Response(response_to_beSend,status=status.HTTP_201_CREATED)
            else:
                return Response(serialized.errors)
        return Response("Your request is empty",status=status.HTTP_400_BAD_REQUEST)
    
    
