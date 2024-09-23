from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from product.templates import*
from Cart.models import cartModel
from UserApp.customPermissions import CustomizeAPIPermissions
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login
from django.contrib.auth import logout
from ShopNow.allSerializers.Userserializers import LoginSerializer
from rest_framework.response import Response
from django.shortcuts import render,redirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.views import View
from ShopNow.allSerializers.Userserializers import WebUserSerializer
from UserApp.models import Webuser
import requests

@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        if request.data:
            serialized = WebUserSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data,status = status.HTTP_201_CREATED)
            else:
                return Response(f"your data is invalid,{serialized.errors}",status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Data is not inluded in request.",status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Invalid method",status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def loginUser(request):
    if request.method =='POST':
        if request.data:
            serialized = LoginSerializer(data = request.data)
            print(request.data)
            if serialized.is_valid():    
                user = authenticate(request,username = serialized.validated_data.get('username'),password=serialized.validated_data.get('password'))
                if user is not None:
                    loged_user = Webuser.objects.get(username = serialized.data.get('username'))
                    print(loged_user)
                    print(user.id,serialized.data.get('username'))
                    logged_user_id = user.id
                    try:
                        cartModel.objects.get(user_of_cart = loged_user)
                    except:
                        try:
                            print("not coming")
                            cartModel.objects.create(user_of_cart = loged_user)
                        except:
                            return Response("cart is causing some issue")
                    refresh_and_access_token = RefreshToken.for_user(user)
                    access_token = str(refresh_and_access_token.access_token)
                    refresh_token = str(refresh_and_access_token)
                    response_to_be_send={
                                'username':serialized.validated_data.get('username'),
                                'access': access_token,
                                'refresh':refresh_token,
                                'logged_user_id':logged_user_id,
                            }
                    return Response(response_to_be_send,status = status.HTTP_200_OK)
                else:
                    return Response("Invalid credentials",status = status.HTTP_404_NOT_FOUND)
            else: 
                return Response(serialized.errors,status = status.HTTP_400_BAD_REQUEST)      
        else: 
            return Response("Request is empty ",status = status.HTTP_400_BAD_REQUEST)    

class RegisteredUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self,request,pk = None):
        if pk is None:
            user = Webuser.objects.all()
            serialized = WebUserSerializer(user,many = True)
            return Response(serialized.data,status=status.HTTP_200_OK)
        else:
            try:
                instance = Webuser.objects.get(id = pk)
            except:
                return Response("User Not exists ",status = status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(request,instance)
            serialized = WebUserSerializer(instance)
            return Response(serialized.data,status = status.HTTP_200_OK) 
           
    def put(self,request,pk = None):
        if pk is not None:
           instance = Webuser.objects.get(id = pk)
           self.check_object_permissions(request,instance)
           data = request.data
           serialized = WebUserSerializer(instance,data = data)
           if serialized.is_valid():
                serialized.save()
                return Response(serialized.data,status = status.HTTP_200_OK)
           else:
                return Response(serialized.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not adding the pk"}, status = status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk = None):
        
        if pk is not None:
            instance=Webuser.objects.get(id = pk)
            self.check_object_permissions(request,instance)
            data = request.data
            serialized = WebUserSerializer(instance,data = data,partial = True)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data,status = status.HTTP_200_OK)
            else:
                return Response(serialized.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response("You are not adding the pk")

    def delete(self,request,pk = None):
            if pk is not None:
                instance = Webuser.objects.get(id = pk)
                self.check_object_permissions(request,instance)
                instance.delete()
                return Response("Deleted successfully!!",status = status.HTTP_200_OK)
            return Response({'respons':"You are not adding the pk"},status = status.HTTP_400_BAD_REQUEST)


class UserAdminFrontend(View): 
    def get(self,request,*args,**kwargs):
        token = request.session.get('access_token')
        pk = kwargs.get('pk')
        if token:
            headers={'Authorization': f"Bearer {token}"}
            if pk is None:              
                if request.user.is_staff:   
                    response_from_api = requests.get("http://127.0.0.1:8000/api/user/",headers = headers)
                    if response_from_api.status_code == 200:
                        response_to_pass = response_from_api.json()
                        user_identity = request.GET.get('admin')
                        if user_identity:
                            return render(request,'users.html',{'response':response_to_pass,'data_reteived':True,'admin':True})
                        else:
                            return render(request,'users.html',{'response':response_to_pass,'data_reteived':True})
                    else:
                        response_to_pass = {}
                        if response_from_api.status_code == 401:
                            massage = "ALERT: You are unauthorized to access this!!!"
                        else:
                            massage = f"Request to retrieve data is failed. status_code: {response_from_api.status_code}"
                        return render(request,'users.html',{'response':response_to_pass,'data_reteived':False,'massage':massage,'single':False})
                else:
                    massage="ALERT!!, only Admin is Allowed to do this action!!"
                    return render(request,'users.html',{'data_reteived':False,'massage':massage,'single':False})
            else:  
                response_from_api = requests.get(f"http://127.0.0.1:8000/api/user/{pk}",headers = headers)
                if response_from_api.status_code == 200:
                    response_to_pass = response_from_api.json()
                    user_identity = request.GET.get('admin')
                    response_from_order = requests.get(f"http://127.0.0.1:8000/api/user_order/{pk}",headers = headers)
                    if response_from_order.status_code == 200:
                        order_history = response_from_order.json()
                        user_identity = request.GET.get('admin')
                        if user_identity:
                            return render(request,'users.html',{'orders':order_history,'response':response_to_pass,
                                                                'orderror':False,'single':True,'admin':True})
                        else:
                             return render(request,'users.html',{'orders':order_history,'response':response_to_pass,
                                                                'orderror':False,'single':True})
                    else:
                        if user_identity:
                            return render(request,'users.html',{'response':response_to_pass,'orderror':True,'single':True,'orders':"You have No orders yet!!",'admin':True})
                        return render(request,'users.html',{'response':response_to_pass,'orderror':True,'single':True,'orders':"You have No orders yet!!",})
                else:
                    response_to_pass = {}
                    if response_from_api.status_code == 401:
                        massage = "ALERT: You are unauthorized to access this!!!"
                    else:
                        massage = f"Request to retrieve data is failed. status_code: {response_from_api.status_code}"
                    return render(request,'users.html',{'response':response_to_pass,'data_reteived':False,'massage':massage})            
        else:
            return HttpResponse("There is No token",status= status.HTTP_401_UNAUTHORIZED)
def home(request):
    token=request.session.get('access_token')
    authenticated_user=request.user.is_authenticated
    if  token and authenticated_user:
        user_id=request.session.get('user_id')
        user_who_requested=request.user
        return render(request,'home.html',{'user_id':user_id,'user':user_who_requested,'viewCart':True})
    else:
        print("could login in first time",token,authenticated_user)
        return render(request,'home.html')

def loginPage(request):
    if request.method == 'GET':
        return render(request,'loginPage.html')
    if request.method == 'POST':
        form_data = request.POST
        print(form_data)
        form_data_dict = {
                        'username':form_data.get('username'),
                        'password':form_data.get('password'),}
        response_from_api = requests.post("http://127.0.0.1:8000/api/login/",data = form_data_dict)
        if response_from_api.status_code == 200:
            response_to_pass = response_from_api.json()
            token = response_to_pass.get('access')
            user_id = response_to_pass.get('logged_user_id')
            request.session['access_token'] = token
            request.session['user_id'] = user_id
            username = form_data_dict.get('username')
            password = form_data_dict.get('password')
            user = authenticate(request,username = username,password = password)
            if user is not None:
                login_user = login(request,user)
                print("Login to home")
                return redirect('/api/home/')
            else:
                return redirect("/api/login_user/")
        else:
            try:
                return render(request,'loginPage.html',{'massage':"NOT login, Please try again!!",'error':True})
            except:
                return Response({'error': 'Invalid JSON response'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            
def registerFrontend(request):
    if request.method == 'GET':
        try:
            return render(request,'registerUser.html',)
        except:
               return render(request,'registerUser.html',)
    if request.method == 'POST':
        form_data = request.POST
        form_data_dict = {
                            'username':form_data.get('username'),
                            'email':form_data.get('email'),
                            'password':form_data.get('password'),
                            'confirm_password':form_data.get('confirm_password'),}
            
        response_from_api = requests.post("http://127.0.0.1:8000/api/register/",data=form_data_dict)
        if response_from_api.status_code == 201:
            response_to_pass = response_from_api.json()
            return render(request,'registerUser.html',{'massage':"User is Registered Successfully!!"})
        else:
            response_to_pass = response_from_api.json()
            return render(request,'registerUser.html',{'massage':response_to_pass})

def updateProfile(request,pk):
    token = request.session.get('access_token')
    if token:
        header = {'Authorization': f"Bearer {token}"}
        if request.method == 'GET':
            if pk is not None:
                    response_from_api = requests.get(f"http://127.0.0.1:8000/api/user/{pk}",headers = header)
                    response_to_pass = response_from_api.json()
                    if response_from_api.status_code == 200:
                        return render(request,'updateUser.html',{'response':response_to_pass})
                    else:
                        if response_from_api.status_code == 401:
                            return render(request,'updateUser.html',{'massage':response_to_pass,'response':response_to_pass,'login':True})
                        return render(request,'updateUser.html',{'massage':response_to_pass,'response':response_to_pass})                        
        if request.method == 'POST':
            if pk is not None:
                data = {'username':request.POST.get('username'),
                        'email':request.POST.get('email'),
                        'password':request.POST.get('password'),
                        'confirm_password':request.POST.get('confirm_password'),}
                response_from_api = requests.put(f"http://127.0.0.1:8000/api/user/{pk}",data = data,headers = header)
                print(response_from_api)
                response_to_pass = response_from_api.json()
                print(response_to_pass)
                if response_from_api.status_code == 200:
                    return render(request,'users.html',{'response':response_to_pass,'data_reteived':True,'single':True,'massage':"Updated Successfully!!"})
                else:
                    if response_from_api.status_code == 401:
                        return render(request,'updateUser.html',{'massage':response_to_pass,'response':response_to_pass,'login':True})

                    return render(request,'updateUser.html',{'massage':f"Try again,{response_to_pass}",'response':response_to_pass})
            else:
                return render(request,'updateUser.html',{'massage':"your pk is None"})
             
def deleteUser(request,pk):
    token = request.session.get('access_token')
    if token:
        header = {'Authorization': f"Bearer {token}"}
        if pk is not None:
            response_from_api = requests.delete(f"http://127.0.0.1:8000/api/user/{pk}",headers = header)
            response_to_pass = response_from_api.json()
            print(response_to_pass)
            if response_from_api.status_code == 200:
                return render(request,'users.html',{'response':response_to_pass,'data_reteived':False,'single':True,'massage':"Deleted Successfully!!"})
            else:
                if response_from_api.status_code == 401:
                    return render(request,'updateUser.html',{'massage':response_to_pass,'response':response_to_pass,'login':True})
                return render(request,'updateUser.html',{'massage':f"Try again,{response_to_pass}",'response':response_to_pass})
        else:
            return render(request,'updateUser.html',{'massage':"your pk is None"})
        
def getUserName(user_id,header):
    response_from_api = requests.get(f"http://127.0.0.1:8000/api/user/{user_id}",headers = header)
    if response_from_api.status_code == 200:
        response_to_pass = response_from_api.json()
        username = response_to_pass.get('username')
        return username
    else:
        return -1
    
def adminLogin(request):
    if request.method == 'GET':
        return render(request,'adminUser.html',)
    if request.method == 'POST':
        form_data = request.POST
        print(form_data)
        form_data_dict = {
                       'username':form_data.get('username'),
                       'password':form_data.get('password'),}
        user = authenticate(username = form_data_dict['username'], password = form_data_dict['password'])
        if user is not None:
            # check_is_admin means only superuserr is allowed to access this page
            if user.is_superuser:
                response_from_api = requests.post("http://127.0.0.1:8000/api/login/",data = form_data_dict)
                if response_from_api.status_code == 200:
                    response_to_pass = response_from_api.json()
                    token = response_to_pass.get('access')
                    user_id = response_to_pass.get('logged_user_id')
                    request.session['access_token'] =  token
                    request.session['user_id'] = user_id
                    username = form_data_dict.get('username')
                    password = form_data_dict.get('password')
                    user = authenticate(request,username=username,password=password)
                    if user:
                        login_user = login(request,user)
                        return render(request,"admin_options.html",{'user_id':user_id})
                    else:
                        return redirect("/api/admin/")
                else:
                    response_to_pass = response_from_api.json()
                    print(response_to_pass)
                    return render(request,'loginPage.html',{'massage':response_to_pass,'error':True})
            else:
                return render(request,'adminUser.html',{'massage':"You are not Authorized only admin can Access!!",'error':True})
        else:
            return render(request,'adminUser.html',{'massage':"User is not in database!!",'error':True})

    
def adminOptions(request):
    token = request.session.get('access_token')
    if token:
        header = {'Authorization': f"Bearer {token}"}
        if request.method == 'GET':
            return render(request,'adminOptions.html',{'user_id':request.session['user_id']})


            
        

              




    



        
