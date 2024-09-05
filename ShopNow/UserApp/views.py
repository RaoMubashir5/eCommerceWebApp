from django.shortcuts import render

# Create your views here.
from UserApp.models import Webuser
from UserApp.serializers import WebUserSerializer,loginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render,redirect
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication

from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.permissions import DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
#Generic API views

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import logout
from django.http import HttpResponseRedirect,Http404,HttpResponse
from rest_framework import viewsets
#it is for model creation
from rest_framework.views import APIView
from django.contrib.auth import authenticate
#import custom permissions class
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from UserApp.customPermissions import CustomizeAPIPermissions
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from Cart.models import cartModel


@csrf_exempt
@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        if request.data:
            serialized=WebUserSerializer(data=request.data)
            if serialized.is_valid():
                serialized.save()
                # print(f"""Username: {serialized.data.get('username')}, Email: {serialized.data.get('useremail')},
                #     Password: {serialized.data.get('password')}, Confirm Password: {serialized.data.get('confirm_password')}""")
                return Response(serialized.data)
            else:
                return Response("your data is invalid")
        else:
            return Response("Data is not inluded in request.")
    else:
        return Response("Invalid method")


       
@csrf_exempt
@api_view(['POST'])
def loginUser(request):
    if request.method=='POST':
        if request.data:
            serialized=loginSerializer(data=request.data)
            print(request.data)
            if serialized.is_valid():
               
                print(serialized.data.get('username'),serialized.validated_data.get('password'))
                user=authenticate(request,username=serialized.validated_data.get('username'),password=serialized.validated_data.get('password'))
                print(user,serialized.data.get('username'))
                loged_user=Webuser.objects.get(username=serialized.data.get('username'))
                print(loged_user)
                if user is not None:
                    try:
                        cartModel.objects.get(user_of_cart=loged_user)
                        pass
                    except:
                        try:
                            print("not coming")
                            cartModel.objects.create(user_of_cart=loged_user)
                        except:
                            return Response("cart is causing some issue")
                    refresh_and_access_token=RefreshToken.for_user(user)
                    access_token = str(refresh_and_access_token.access_token)
                    refresh_token = str(refresh_and_access_token)
                    response_to_be_send={
                                'username':serialized.validated_data.get('username'),
                                'access': access_token,
                                'refresh':refresh_token,
                            }
                    return Response(response_to_be_send)
                else:
                    return Response("invalid credentials")

            else: 
                return Response(serialized.errors)      
             


class get_register_users(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]

    def get(self,request,pk=None):
        if pk is None:
            user=Webuser.objects.all()
            serialized=WebUserSerializer(user,many=True)
            print("This is user: ",request.user)
            return Response({'user':serialized.data})
            
        
        else:
            instance=Webuser.objects.get(id=pk)
            self.check_object_permissions(request,instance)
            user=Webuser.objects.get(id=pk)
            serialized=WebUserSerializer(user,many=False)
            return Response({'user':serialized.data})
    def put(self,request,pk=None):
        print(pk)
        if pk is not None:
           instance=Webuser.objects.get(id=pk)
           self.check_object_permissions(request,instance)
           data= request.data
           serialized=WebUserSerializer(instance,data=data)
           if serialized.is_valid():
                serialized.save()
                return Response(serialized.data,status=status.HTTP_200_OK)
        return Response("You are not adding the pk")

    def patch(self,request,pk=None):
        
        if pk is not None:
            instance=Webuser.objects.get(id=pk)
            self.check_object_permissions(request,instance)
            data= request.data
            serialized=WebUserSerializer(instance,data=data,partial=True)
            if serialized.is_valid():
                    print("validete nhi hoa")
                    serialized.save()
                    return Response(serialized.data,status=status.HTTP_200_OK)
            else:
                return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response("You are not adding the pk")

    def delete(self,request,pk=None):
            if pk is not None:
                instance=Webuser.objects.get(id=pk)
                self.check_object_permissions(request,instance)
                instance.delete()
                return Response(status=status.HTTP_200_OK)
            return Response("You are not adding the pk")

        
    