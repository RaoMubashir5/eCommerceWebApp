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

from django.views import View
import requests



@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        if request.data:
            serialized=WebUserSerializer(data=request.data)
            if serialized.is_valid():
                serialized.save()
                # print(f"""Username: {serialized.data.get('username')}, Email: {serialized.data.get('useremail')},
                #     Password: {serialized.data.get('password')}, Confirm Password: {serialized.data.get('confirm_password')}""")
                return Response(serialized.data,status=status.HTTP_201_CREATED)
            else:
                return Response(f"your data is invalid,{serialized.errors}",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Data is not inluded in request.",status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Invalid method",status=status.HTTP_400_BAD_REQUEST)


       

@api_view(['POST'])
def loginUser(request):
    if request.method=='POST':
        if request.data:
            serialized=loginSerializer(data=request.data)
            print(request.data)
            if serialized.is_valid():
               
                # print(serialized.data.get('username'),serialized.validated_data.get('password'))
                user=authenticate(request,username=serialized.validated_data.get('username'),password=serialized.validated_data.get('password'))
                print(user.id,serialized.data.get('username'))
                logged_user_id=user.id
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
                                'logged_user_id':logged_user_id,
                            }
                    return Response(response_to_be_send,status=status.HTTP_200_OK)
                else:
                    return Response("invalid credentials",status=status.HTTP_404_NOT_FOUND)

            else: 
                return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)      
             


class get_register_users(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]

    def get(self,request,pk=None):
        if pk is None:
            user=Webuser.objects.all()
            serialized=WebUserSerializer(user,many=True)
            print("This is user: ",request.user)
            return Response(serialized.data)
        else:
            print("kuvh")
            try:
                instance=Webuser.objects.get(id=pk)
            except:
                return Response("User Not exists ",status=status.HTTP_404_NOT_FOUND)
            print("......",instance,"........")
            self.check_object_permissions(request,instance)
            serialized=WebUserSerializer(instance)
            return Response(serialized.data)
           
           
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


#These are for frontEnd.
class UserAdminFrontend(View):

    def get(self,request,*args,**kwargs):
        token=request.session.get('access_token')
        pk=request.session.get('user_id')
        if token:
            headers={'Authorization': f"Bearer {token}"}
            #decoding the token to extract the userr id :
            #decode_token=JWT

            print(headers)
        #   pk=kwargs.get('pk')
        #     if pk is None:
               
        #         response_from_api=requests.get("http://127.0.0.1:8000/api/user/",headers=headers)
        #         if response_from_api.status_code==200:
        #             response_to_pass=response_from_api.json()
 
        #             return render(request,'users.html',{'response':response_to_pass,'data_reteived':True})
        #         else:
        #             print("Status code: ",response_from_api.status_code)
        #             response_to_pass={}
        #             if response_from_api.status_code==401:
        #                 massage="ALERT: You are unauthorized to access this!!!"
        #             else:
        #                 massage=f"Request to retrieve data is failed. status_code: {response_from_api.status_code}"
        #             return render(request,'users.html',{'response':response_to_pass,'data_reteived':False,'massage':massage})
        #     else:
        #         print(pk,request.user.is_superuser)
            print("...........",pk)
            response_from_api=requests.get(f"http://127.0.0.1:8000/api/user/",headers=headers)
            if response_from_api.status_code==200:
                response_to_pass=response_from_api.json()
                return render(request,'users.html',{'response':response_to_pass,'data_reteived':True})
            else:
                print("Detail Status code: ",response_from_api.status_code)
                response_to_pass={}
                if response_from_api.status_code==401:
                    massage="ALERT: You are unauthorized to access this!!!"
                else:
                    massage=f"Request to retrieve data is failed. status_code: {response_from_api.status_code}"
                return render(request,'users.html',{'response':response_to_pass,'data_reteived':False,'massage':massage})            
        else:
            return HttpResponse("There is No token",status= status.HTTP_401_UNAUTHORIZED)
def home(request):
    if request.session.get('access_token'):
        print(request.session.get('user_id'),request.session.get('access_token'))
        return render(request,'home.html',{'user_id':request.session.get('user_id')})

def login_page(request):
    if request.method=='GET':
        return render(request,'loginPage.html')
    if request.method=='POST':
        form_data=request.POST
        print(form_data)
        form_data_dict={
                       'username':form_data.get('username'),
                       'password':form_data.get('password'),}
        response_from_api=requests.post("http://127.0.0.1:8000/api/login/",data=form_data_dict)
        if response_from_api.status_code==200:
            response_to_pass=response_from_api.json()
            request.session['access_token']=response_to_pass.get('access')
            request.session['user_id']=response_to_pass.get('logged_user_id')
            print(request.session['access_token'])
            print("......",request.session['user_id'])
            return redirect("/api/home/")
        else:
            response_to_pass=response_from_api.json()
            print(response_to_pass)
            return render(request,'login_user.html',{'massage':response_to_pass})



def registerFrontend(request):
       
            
            if request.method=='GET':
                try:
                    print("Token aya hoa ha:",request.session.get('access_token'))
                    return render(request,'registerUser.html',)
                except:
                    return render(request,'registerUser.html',)
            if request.method=='POST':
                form_data=request.POST
                print(form_data)
                form_data_dict={
                'username':form_data.get('username'),
                'email':form_data.get('email'),
                'password':form_data.get('password'),
                'confirm_password':form_data.get('confirm_password'),
                }
                response_from_api=requests.post("http://127.0.0.1:8000/api/register/",data=form_data_dict)
                if response_from_api.status_code==201:
                    response_to_pass=response_from_api.json()
                    
                    return render(request,'registerUser.html',{'massage':"User is Registered Successfully!!"})
                else:
                    response_to_pass=response_from_api.json()
                    print(response_to_pass)
                    return render(request,'registerUser.html',{'massage':response_to_pass})
       

            


        
