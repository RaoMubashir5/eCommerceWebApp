from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from Cart.models import CartModel
from django.views.decorators.csrf import csrf_exempt
from UserApp.customPermissions import CustomizeAPIPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from ShopNow.allSerializers.Userserializers import LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ShopNow.allSerializers.Userserializers import WebUserSerializer
from UserApp.models import Webuser
import requests

@api_view(['POST'])
def register_user(request):
            serialized = WebUserSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response(f"your data is invalid, {serialized.errors}", status = status.HTTP_400_BAD_REQUEST)
            
@api_view(['POST'])
def login_user(request):
            serialized = LoginSerializer(data = request.data)
            if serialized.is_valid():
                username = serialized.validated_data.get('username')
                password = serialized.validated_data.get('password')
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    loged_user = Webuser.objects.get(username = username)
                    logged_user_id = user.id
                    try:
                        CartModel.objects.get(user_of_cart = loged_user)
                    except:
                        try:
                            CartModel.objects.create(user_of_cart = loged_user)
                        except:
                            return Response("cart is causing some issue")
                    response_to_be_send = get_token(user, username, logged_user_id)
                    return Response(response_to_be_send, status = status.HTTP_200_OK)
                else:
                    return Response("Invalid credentials", status = status.HTTP_404_NOT_FOUND)
            else: 
                return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)      
        
def get_token(user, username, id):
    refresh_and_access_token = RefreshToken.for_user(user)
    access_token = str(refresh_and_access_token.access_token)
    refresh_token = str(refresh_and_access_token)
    response_to_be_send = {
                         'username': username,
                         'access': access_token,
                         'refresh': refresh_token,
                        'logged_user_id': user.id
                        }
    return response_to_be_send
                                        
class GetSingleUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request, pk = None):
                try:
                    instance = Webuser.objects.get(id = pk)
                except:
                    return Response("User Not exists ", status = status.HTTP_404_NOT_FOUND)
                self.check_object_permissions(request, instance)
                serialized = WebUserSerializer(instance)
                return Response(serialized.data) 
    
class GetRegisterterdUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request):
        user = Webuser.objects.all()
        serialized = WebUserSerializer(user, many = True)
        return Response(serialized.data)

class UpdateUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def put(self, request, pk = None):
        instance = Webuser.objects.get(id = pk)
        self.check_object_permissions(request, instance)
        data = request.data
        serialized = WebUserSerializer(instance, data = data)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)   
        serialized.save()
        return Response(serialized.data)                   
    
    def patch(self, request, pk = None):
        instance=Webuser.objects.get(id = pk)
        self.check_object_permissions(request, instance)
        data = request.data
        serialized = WebUserSerializer(instance, data = data, partial = True)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)   
        serialized.save()
        return Response(serialized.data)   

class DeleteUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def delete(self, request, pk = None):
            try:
                instance = Webuser.objects.get(id = pk)
            except:
                return Response({'out':"User not even exists!!"},status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(request, instance)
            instance.delete()
            return Response({'out':"Deleted successfully!!"})
