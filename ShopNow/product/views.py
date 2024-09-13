from django.shortcuts import render,redirect,HttpResponse

from product.models import product

from product.serializer import productSerializer

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import View
# Import the authetications and permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from .customPermissions import CustomizeAPIPermissions
import requests
class productView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]
    def post(self,request):
        
        if request.data:
            print(request.data)
           
            self.check_permissions(request)
            serialized=productSerializer(data=request.data)

            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"Invalid data {serialized.errors} .",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Request is empty,No data!! ")

    def get(self,request,pk=None):
        if pk is None:
            products=product.objects.all()
            serialized=productSerializer(products,many=True)
            return Response(serialized.data,status=status.HTTP_200_OK)
        else:
            
            # try:
            instance=product.objects.get(id=pk)
            print("Response",self.check_object_permissions(request,instance))
            # except:
            #     return Response("Product does not exists!!")
            serialized=productSerializer(instance,many=False)
            return Response(serialized.data)
    def put(self,request,pk=None):
        if pk is not None:
            instance=product.objects.get(id=pk)
            self.check_object_permissions(request,instance)
            if request.data:
                serialized=productSerializer(instance,data=request.data)
                if serialized.is_valid():
                    serialized.save()
                    return Response(serialized.data, status=status.HTTP_200_OK)
                else:
                    print("........",serialized.errors,"............")
                    return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Request is empty",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("pk is None",status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self,request,pk=None):
        if pk is not None:
            instance=product.objects.get(id=pk)
            self.check_object_permissions(request,instance)
            if request.data:
                serialized=productSerializer(instance,data=request.data,partial=True)
                if serialized.is_valid():
                    serialized.save()
                    return Response(serialized.data, status=status.HTTP_200_OK)
                else:
                    return Response(f"Ivalid data{serialized.errors}",status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Request is empty",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("pk is None")
        
    def delete(self,request,pk=None):
        if pk is not None:
            instance=product.objects.get(id=pk)
            self.check_object_permissions(request,instance)
            try:
                instance.delete()
                return Response("Deleted successfully.")
            except Exception as e:
                Response({'issue':e},status=status.HTTP_400_BAD_REQUEST)
            


class ListProducts(View):

    def get(self,request,*args,**kwargs):

        token=request.session.get('access_token')
        pk =kwargs.get('pk')
        print(pk)
        if token:
            headers={'Authorization': f"Bearer {token}"}
            #decoding the token to extract the userr id :
            #decode_token=JWT
            print("............",headers,pk)
            if pk is None:
                requesting_response=requests.get(f"http://127.0.0.1:8000/api/product/",headers=headers)
                response_in_json=requesting_response.json()
                print(response_in_json)
                if requesting_response.status_code==200:
                    return render(request,'listProduct.html',{'products':response_in_json})
                else:
                    if requesting_response.status_code==401:
                        return redirect('/api/home/')
                    return redirect('/api/listProduct.html/')

def delete_Product(request,pk):
    token=request.session.get('access_token')
    print(pk)
    if token:
        headers={'Authorization': f"Bearer {token}"}
        print("............",headers,pk)
        requesting_response=requests.delete(f"http://127.0.0.1:8000/api/product/{pk}",headers=headers)
        response_in_json=requesting_response.json()
        if requesting_response.status_code==200:
            requesting_response=requests.get(f"http://127.0.0.1:8000/api/product/",headers=headers)
            response_in_json=requesting_response.json()
            if requesting_response.status_code==200:
                return render(request,'listProduct.html',{'products':response_in_json,'success':"Product deleted successfully!!",'error':False})
            else:
                if requesting_response.status_code==401:
                    return redirect('/api/home/')
                return render(request,'listProduct.html',{'products':response_in_json,'massage':"Product Not deleted!!",'error':True})

        else:
            if requesting_response.status_code==401:
                return redirect('/api/home/')
            return render(request,'listProduct.html',{'products':response_in_json,'massage':"Product Not deleted!!",'error':True})
    else:
        return redirect('/api/home/')


def update_Product(request,pk):
    token=request.session.get('access_token')
    print(pk)
    if token:
        headers={'Authorization': f"Bearer {token}"}
        if request.method=='GET':
            requesting_response=requests.get(f"http://127.0.0.1:8000/api/product/{pk}",headers=headers)
            response_in_json=requesting_response.json()
            print("::::::::::GEt>>>>>>>>>",response_in_json,":::::::::::::::::::::<<<<<<<")
            if requesting_response.status_code==200:
                return render(request,'updateProduct.html',{'product':response_in_json})
            else:
                return redirect('/api/admin_options/')
        if request.method=='POST':
            data={
            'product_name':request.POST.get('product_name'),
            'product_description':request.POST.get('product_description'),
            'price':request.POST.get('price'),}
            files = {
            'product_image': request.FILES.get('product_image',), }

            print("............",headers,pk,data,files)
            
            if not files['product_image'] or not data['price'] or not data['product_name'] or not data['product_description']:
                print("......,.,.,.,.,..,.####..Pathch......3###3333333")
                requesting_response=requests.patch(f"http://127.0.0.1:8000/api/product/{pk}",data=data,files=files,headers=headers)
            else:
                requesting_response=requests.put(f"http://127.0.0.1:8000/api/product/{pk}",data=data,files=files,headers=headers)                
            try:
                response_in_json=requesting_response.json()
            except:
                print("::::::::::;>>>>>>>>>",response_in_json)
            if requesting_response.status_code==200:
                requesting_response=requests.get(f"http://127.0.0.1:8000/api/product/",headers=headers)
                response_in_json=requesting_response.json()
                if requesting_response.status_code==200:
                    return render(request,'listProduct.html',{'products':response_in_json,'success':"Product Updated successfully!!",'error':False})
                else:
                    if requesting_response.status_code==401:
                        return redirect('/api/home/')
                    return render(request,'listProduct.html',{'products':response_in_json,'massage':"Product Not updated!!",'error':True})
            else:
                if requesting_response.status_code==401:
                    return redirect('/api/home/')
                return render(request,'updateProduct.html',{'massage':f"Product Not updated!!{response_in_json} .",'error':True})
        else:
            return redirect('/api/home/')

def add_product(request):
    token=request.session.get('access_token')
    if token:
        headers={'Authorization': f"Bearer {token}"}
        if request.method=='GET':
            return render(request,'add_product.html')
        if request.method=='POST':
            data={
            'product_name':request.POST.get('product_name'),
            'product_description':request.POST.get('product_description'),
            'price':request.POST.get('price'),}
            files = {
            'product_image': request.FILES.get('product_image'), }
            print("............",headers,data)
            requesting_response=requests.post(f"http://127.0.0.1:8000/api/product/",data=data,files=files,headers=headers)
            response_in_json=requesting_response.json()
            if requesting_response.status_code==201:
                return render(request,'add_product.html',{'massage':f"Product Added successfully!!{response_in_json}"})
            else:
                if requesting_response.status_code==401:
                    return redirect('/api/home/')
                return render(request,'add_product.html',{'massage':f"Product Not Added!! {response_in_json}"})


def products_list_for_user(request):
        try:
            token=request.session.get('access_token')
        except:
            return redirect('/api/home/')
        if token:
            headers={'Authorization': f"Bearer {token}"}
            #decoding the token to extract the userr id :
            #decode_token=JWT
            print("............",headers)
            requesting_response=requests.get(f"http://127.0.0.1:8000/api/product/",headers=headers)
            response_in_json=requesting_response.json()
            print(";;;;;;;;;;;;;",response_in_json)
            if requesting_response.status_code==200:
                return render(request,'products_list.html',{'products':response_in_json})
            else:
                if requesting_response.status_code==401:
                    return redirect('/api/home/')
        return redirect('/api/home/')


         
  
    
        
    
       



