from rest_framework.views import APIView
from .customPermissions import CustomizeAPIPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from product.models import Product
from ShopNow.allSerializers.productSerializer import ProductSerializer
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import View
import math
import requests

class ProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def post(self, request):
        if request.data:
            self.check_permissions(request)
            serialized = ProductSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response(f"Invalid data {serialized.errors} .", status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Request is empty,No data!! ")

    def get(self, request, pk = None):
        if pk is None:
            sort_by = request.GET.get('sort_order')
            if sort_by:
                if sort_by == 'low_to_high':
                    products = Product.objects.all().order_by('price')
                else:
                    products = Product.objects.all().order_by('-price')
            else:
                products = Product.objects.all()
            products_per_pages = 3
            total_products = products.count()
            total_pages = math.ceil(total_products/products_per_pages)
            page_number = 1
            param_page_number = request.GET.get('page')
            if param_page_number != 'None' and param_page_number is not None:
                paginator = Paginator(products, products_per_pages)
                page_number = int(param_page_number)        
                if page_number > total_pages:
                    products = paginator.get_page(1)
                    page_number = 1
                else:
                    products = paginator.get_page(page_number)
            serialized = ProductSerializer(products, many = True)
            return Response({'page_number':page_number, 'total_pages':total_pages, 'products': serialized.data}, status = status.HTTP_200_OK)
        else:
            instance = Product.objects.filter(id = pk)
            if instance.exists():
                self.check_object_permissions(request, instance[0])
                serialized = ProductSerializer(instance[0])
                return Response(serialized.data, status=status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_404_NOT_FOUND)
    def put(self, request,pk = None):
        if pk is not None:
            instance = Product.objects.get(id = pk)
            self.check_object_permissions(request, instance)
            if request.data:
                serialized = ProductSerializer(instance, data = request.data)
                if serialized.is_valid():
                    serialized.save()
                    return Response(serialized.data, status = status.HTTP_200_OK)
                else:
                    return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Request is empty", status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("pk is None", status = status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request,pk = None):
        if pk is not None:
            instance = Product.objects.get(id = pk)
            self.check_object_permissions(request, instance)
            if request.data:
                serialized = ProductSerializer(instance, data = request.data, partial = True)
                if serialized.is_valid():
                    serialized.save()
                    return Response(serialized.data, status = status.HTTP_200_OK)
                else:
                    return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Request is empty", status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("pk is None")
        
    def delete(self, request, pk = None):
        if pk is not None: 
            instance = Product.objects.get(id = pk)
            self.check_object_permissions(request, instance)
            try:
                instance.delete()
                return Response("Deleted successfully.")
            except Exception as e:
                Response({'issue':e}, status=status.HTTP_400_BAD_REQUEST)

class SearchApiByName(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request, product_name):
            instance = Product.objects.filter(product_name__icontains = product_name)
            if instance.exists():
                self.check_object_permissions(request, instance[0])
                serialized = ProductSerializer(instance[0])
                return Response(serialized.data, status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_404_NOT_FOUND)

class ListProducts(View):

    def get(self, request, *args, **kwargs):
        token = request.session.get('access_token')
        pk = kwargs.get('pk')
        if token:
            headers = {'Authorization': f"Bearer {token}"}
            sort_order = request.GET.get('sort')
            page = request.GET.get('page')
            requesting_response = requests.get(f"http://127.0.0.1:8000/api/product/?sort_order={sort_order}&page={page}", headers = headers)
            if requesting_response.status_code == 200:
                response_in_json = requesting_response.json()
                products = response_in_json.get('products')
                page_number = response_in_json.get('page_number')
                total_page = response_in_json.get('total_pages')
                if total_page > page_number:
                    next = page_number + 1
                    prev = page_number - 1                
                elif total_page == page_number:
                    next = 0
                    if page_number > 1 :
                        prev = page_number - 1
                    else:
                        prev = 0
                return render(request, 'listProduct.html', {'products':products, 'next':next, 'prev':prev,
                                                            'page_number':page_number, 'sort':sort_order})
            else:
                if requesting_response.status_code == 401:
                    return redirect('/api/home/')
                return redirect('/api/listproduct/')
        else:
            return redirect('/api/home/')

def search(request):
        token = request.session.get('access_token')
        if token:
            headers = {'Authorization': f"Bearer {token}"}
            Query_param = request.POST.get('product_name')
            requesting_response = requests.get(f"http://127.0.0.1:8000/api/search/{Query_param}", headers = headers)
            if requesting_response.status_code == 200:
                response_in_json = requesting_response.json()
                print("Returned :", response_in_json)
                if request.GET.get('product'):
                    return render(request, 'searchedProductForUser.html', {'product': response_in_json})
                else:
                    return render(request, 'singleSearchedProduct.html', {'product': response_in_json})
            else:
                if requesting_response.status_code == 401:
                    return redirect('/api/home/')
                if request.GET.get('product'):
                    return render(request, 'searchedProductForUser.html', {'massage': "Product Not found!!"})
                else:
                    return render(request, 'singleSearchedProduct.html', {'massage': "Product Not found!!"})

def delete_Product(request, pk):
    token = request.session.get('access_token')
    if token:
        headers = {'Authorization': f"Bearer {token}"}
        requesting_response = requests.delete(f"http://127.0.0.1:8000/api/product/{pk}", headers = headers)
        response_in_json = requesting_response.json()
        if requesting_response.status_code == 200:
            return redirect('/api/listproduct/?page=1')
        else:
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
            return render(request, 'listProduct.html', {'products':response_in_json, 'massage':"Product Not deleted!!", 'error':True})
    else:
        return redirect('/api/home/')
    
def update_Product(request, pk):
    token = request.session.get('access_token')
    if token:
        headers = {'Authorization': f"Bearer {token}"}
        if request.method == 'GET':
            requesting_response = requests.get(f"http://127.0.0.1:8000/api/product/{pk}", headers = headers)
            if requesting_response.status_code == 200:
                response_in_json = requesting_response.json()
                return render(request, 'updateProduct.html', {'product':response_in_json})
            else:
                return redirect('/api/admin_options/')
        if request.method == 'POST':
            data={
                'product_name': request.POST.get('product_name'),
                'product_description': request.POST.get('product_description'),
                'price': request.POST.get('price')}
            files = {
                    'product_image': request.FILES.get('product_image')}
            if not files['product_image'] or not data['price'] or not data['product_name'] or not data['product_description']:
                requesting_response = requests.patch(f"http://127.0.0.1:8000/api/product/{pk}", data = data, files = files, headers = headers)
            else:
                requesting_response = requests.put(f"http://127.0.0.1:8000/api/product/{pk}", data = data, files = files, headers = headers)
            if requesting_response.status_code == 200:
                    return redirect('/api/listproduct/?page=1')
            else:
                if requesting_response.status_code == 401:
                    return redirect('/api/home/')
                return render(request, 'updateProduct.html', {'massage': f"Product Not updated!!.", 'error': True})
        else:
            return redirect('/api/home/')

def add_product(request):
    token = request.session.get('access_token')
    if token:
        headers = {'Authorization': f"Bearer {token}"}
        if request.method == 'GET':
            return render(request, 'add_product.html')
        if request.method == 'POST':
            data={
                'product_name': request.POST.get('product_name'),
                'product_description': request.POST.get('product_description'),
                'price': request.POST.get('price'),}
            files = {
                    'product_image': request.FILES.get('product_image')}
            requesting_response = requests.post(f"http://127.0.0.1:8000/api/product/", data = data, files = files, headers = headers)
            response_in_json = requesting_response.json()
            if requesting_response.status_code == 201:
                return render(request, 'add_product.html', {'massage': f"Product Added successfully!!{response_in_json}"})
            else:
                if requesting_response.status_code == 401:
                    return redirect('/api/home/')
                return render(request, 'add_product.html', {'massage':f"Product Not Added!! {response_in_json}"})

def products_list_for_user(request):
        try:
            token = request.session.get('access_token')
        except:
            return redirect('/api/home/')
        if token:
            headers = {'Authorization': f"Bearer {token}"}
            sort_order = request.GET.get('sort')
            page = request.GET.get('page')
            requesting_response = requests.get(f"http://127.0.0.1:8000/api/product/?sort_order={sort_order}&page={page}", headers = headers)
            if requesting_response.status_code == 200:
                response_in_json = requesting_response.json()
                products = response_in_json.get('products')
                page_number = response_in_json.get('page_number')
                total_page = response_in_json.get('total_pages')
                if total_page > page_number:
                    next = page_number + 1
                    prev = page_number - 1
                elif total_page == page_number:
                    next = 0
                    if page_number > 1 :
                        prev = page_number - 1
                    else:
                        prev = 0
                return render(request, 'products_list.html', {'products': products,'next': next,
                               'prev': prev, 'page_number': page_number, 'sort': sort_order})
            else:
                if requesting_response.status_code == 401:
                    return redirect('/api/home/')
        return redirect('/api/home/')


         
  
    
        
    
       



