from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from rest_framework import status
from ShopNow.allSerializers.Userserializers import email_sending_function
from django.views import View
import requests


class SingleUserDetails(View): 

    def get(self, request, pk = None):
        token = request.session.get('access_token')
        if not token:
            return HttpResponse("There is No token", status = status.HTTP_401_UNAUTHORIZED)
        headers = {'Authorization': f"Bearer {token}"}
        response_from_api = requests.get(f"http://127.0.0.1:8000/api/userDetail/{pk}", headers = headers)
        if response_from_api.status_code != 200:
            response_to_pass = {}
            if response_from_api.status_code != 401:
                massage = "ALERT: You are unauthorized to access this!!!"
            else:
                massage = f"Request to retrieve data is failed. status_code: {response_from_api.status_code}"
            context={
                    'response': response_to_pass, 
                    'data_reteived': False,
                    'massage': massage}
            return render(request, 'users.html', context)             
        response_to_pass = response_from_api.json()
        user_identity = request.GET.get('admin')
        response_from_order = requests.get(f"http://127.0.0.1:8000/api/user_order/{pk}", headers = headers)
        if response_from_order.status_code != 200:
            context = {
            'response': response_to_pass,
            'orderror': True,
            'single': True,
            'orders': "You have No orders yet!!"
            }
            if user_identity:
                context['admin'] = True
            return render(request, 'users.html', context)
        order_history = response_from_order.json()
        user_identity = request.GET.get('admin')
        context = {
                'orders':order_history,
                'response':response_to_pass,
                'orderror':False,
                'single':True
                }
        if not user_identity:
            return render(request, 'users.html',context)
        context['admin'] = True
        return render(request, 'users.html', context)
        
class AllUsersDetails(View): 
    def get(self, request):
        token = request.session.get('access_token')
        if not token:
            return HttpResponse("There is No token", status = status.HTTP_401_UNAUTHORIZED)
        headers = {'Authorization': f"Bearer {token}"}
        if not request.user.is_staff: 
            massage="ALERT!!, only Admin is Allowed to do this action!!"
            return render(request, 'users.html', {'data_reteived':False, 'massage':massage, 'single':False}) 
        response_from_api = requests.get("http://127.0.0.1:8000/api/user/", headers = headers)
        if response_from_api.status_code != 200:
            response_to_pass = {}
            if response_from_api.status_code == 401:
                massage = "ALERT: You are unauthorized to access this!!!"
            else:
                massage = f"Request to retrieve data is failed. status_code: {response_from_api.status_code}"
            return render(request, 'users.html', {'response':response_to_pass, 'data_reteived':False, 'massage':massage, 'single':False})
        response_to_pass = response_from_api.json()
        user_identity = request.GET.get('admin')
        if user_identity:
            return render(request, 'users.html', {'response':response_to_pass, 'data_reteived':True, 'admin':True})
        else:
            return render(request, 'users.html', {'response':response_to_pass, 'data_reteived':True})                        
                              
def home(request):
    token = request.session.get('access_token')
    authenticated_user=request.user.is_authenticated
    print(request.user)
    if  token and authenticated_user:
        user_id=request.session.get('user_id')
        user_who_requested=request.user
        return render(request, 'home.html', {'user_id': user_id, 'user': user_who_requested, 'viewCart': True})
    return render(request, 'home.html')
    
def login_page(request):
    if request.method == 'GET':
        return render(request, 'loginPage.html')
    if request.method == 'POST':
        form_data = request.POST
        form_data_dict = {
                        'username':form_data.get('username'),
                        'password':form_data.get('password')
                    }
        response_from_api = requests.post("http://127.0.0.1:8000/api/login/", data = form_data_dict)
        if response_from_api.status_code != 200:
            return render(
                    request,
                    'loginPage.html', 
                    {
                      'massage': "NOT login, Please try again!!",
                      'error': True
                    }
                )
        response_to_pass = response_from_api.json()
        token = response_to_pass.get('access')
        user_id = response_to_pass.get('logged_user_id')
        username = form_data_dict.get('username')
        password = form_data_dict.get('password')
        user = authenticate(request, username = username, password = password)
        if user is None:
            return redirect("/api/login_user/")
        login_user = login(request, user)
        request.session['access_token'] = token
        request.session['user_id'] = user_id
        request_token = request.session.get('access_token')
        if not request_token:
            print("Token is not included", token, request_token)
            return redirect('/api/login_user/')
        print("Login to home")
        return redirect('/api/home/')            
            
def user_registeration(request):
    if request.method == 'GET':
        try:
            return render(request, 'registerUser.html')
        except:
               return render(request, 'registerUser.html')
    if request.method == 'POST':
        form_data = request.POST
        form_data_dict = {
                            'username':form_data.get('username'),
                            'email':form_data.get('email'),
                            'address':form_data.get('address'),
                            'password':form_data.get('password'),
                            'confirm_password':form_data.get('confirm_password')
                        }
        response_from_api = requests.post("http://127.0.0.1:8000/api/register/", data = form_data_dict)
        if response_from_api.status_code != 201:
            return render(
                request, 
                'registerUser.html', 
                {'massage': "Error: User is not created !!"}
            )
        return render(
            request,
            'registerUser.html',
            {'massage': "User is Registered Successfully!!"}
        )       

def update_profile(request, pk):
    token = request.session.get('access_token')
    if not token:
        return redirect('/api/home/')
    header = {'Authorization': f"Bearer {token}"}
    if request.method == 'GET':
        response_from_api = requests.get(f"http://127.0.0.1:8000/api/userDetail/{pk}", headers = header)
        response_to_pass = response_from_api.json()
        if response_from_api.status_code != 200:
            if response_from_api.status_code == 401:
                 return render(
                                request,
                                'updateUser.html',
                                {
                                    'massage': response_to_pass,
                                    'response': response_to_pass,
                                    'login': True
                                }
                            )
            return render(request, 'updateUser.html', {'massage': response_to_pass, 'response': response_to_pass})                        
        return render(request, 'updateUser.html', {'response': response_to_pass})
    
    if request.method == 'POST':               
            data = {'username':request.POST.get('username'),
                    'email':request.POST.get('email'),
                    'address':request.POST.get('address'),
                    'password':request.POST.get('password'),
                    'confirm_password':request.POST.get('confirm_password')}
            response_from_api = requests.put(f"http://127.0.0.1:8000/api/updateUser/{pk}", data = data, headers = header)
            response_to_pass = response_from_api.json()
            if response_from_api.status_code != 200:
                if response_from_api.status_code == 401:
                    return render(
                            request,
                            'updateUser.html',
                            {
                                'massage':response_to_pass, 
                                'response':response_to_pass,
                                'login':True
                            }
                        )
                return render(
                        request,
                        'updateUser.html',
                            {
                                'massage': f"Try again, {response_to_pass}",
                                'response':response_to_pass
                            }
                        )
            return render(
                    request,
                    'users.html',
                        {
                            'response':response_to_pass,
                            'data_reteived':True,
                            'single':True,
                            'massage': "Updated Successfully!!"             
                        }
                    )
   
def delete_user(request, pk = None):
    token = request.session.get('access_token')
    if not token:
        return redirect('/api/home/')
    header = {'Authorization': f"Bearer {token}"}
    response_from_api = requests.delete(f"http://127.0.0.1:8000/api/DeleteUser/{pk}", headers = header)
    if response_from_api.status_code != 200:
        if response_from_api.status_code == 401:
            return redirect('/api/home/')
        return render(request, 'users.html', {'massage':"Try again, User is not Deleted"})
    response_to_pass = response_from_api.json().get('out')
    return render(request, 'users.html', {'response':response_to_pass, 'data_reteived':False, 'single':True, 'massage':"Deleted Successfully!!"})
        
def get_user_name(user_id, header):
    response_from_api = requests.get(f"http://127.0.0.1:8000/api/userDetail/{user_id}", headers = header)
    if response_from_api.status_code == 200:
        response_to_pass = response_from_api.json()
        username = response_to_pass.get('username')
        return username
    else:
        return -1
    
def admin_login(request):
    if request.method == 'GET':
        return render(request, 'adminUser.html')
    
    if request.method == 'POST':
        form_data = request.POST
        form_data_dict = {
                       'username':form_data.get('username'),
                       'password':form_data.get('password'),}
        user = authenticate(username = form_data_dict['username'], password = form_data_dict['password'])
        if user is None:
            return render(request, 'adminUser.html', {'massage': "User is not in database!!", 'error': True})
        if not user.is_superuser:
            return render(request, 'adminUser.html', {'massage': "You are not Authorized only admin can Access!!", 'error': True})
        response_from_api = requests.post("http://127.0.0.1:8000/api/login/", data = form_data_dict)
        if response_from_api.status_code != 200:
            response_to_pass = response_from_api.json()
            return render(request, 'loginPage.html', {'massage': response_to_pass, 'error': True})
        response_to_pass = response_from_api.json()
        token = response_to_pass.get('access')
        user_id = response_to_pass.get('logged_user_id')
        username = form_data_dict.get('username')
        password = form_data_dict.get('password')
        user = authenticate(request, username = username, password = password)
        if user is None:
            return redirect("/api/admin/")
        login_user = login(request, user)
        request.session['access_token'] =  token
        request.session['user_id'] = user_id
        if not request.session.get('access_token'):
            return redirect('/api/admin/')
        return redirect('/api/admin_options/')

def admin_options(request):
    token = request.session.get('access_token')
    if token:
        header = {'Authorization': f"Bearer {token}"}
        if request.method == 'GET':
            return render(request,'admin_options.html', {'user_id': request.session['user_id']})


# Helper functions to reduce the code repitation:

def run_api_data(url, headers, method = 'GET', data = None, files = None):
    if method == 'GET':
        return requests.get(url, headers = headers)
    elif method == 'PUT':
        return requests.put(url, data = data, headers = headers,)
    elif method == 'POST':
        return requests.put(url, data = data, headers = headers,)
    
        

              




    



        
