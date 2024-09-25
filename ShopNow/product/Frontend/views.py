from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import View
import requests


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
                prev, next = update_next_previous(total_page, page_number)
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

def update_next_previous(total_page, page_number):
    if total_page > page_number:
        next = page_number + 1
        prev = page_number - 1                
    elif total_page == page_number:
        next = 0
        if page_number > 1 :
            prev = page_number - 1
        else:
            prev = 0
    return prev,next

def delete_Product(request, pk):
    token = request.session.get('access_token')
    if not token:
        return redirect('/api/home/')
    headers = {'Authorization': f"Bearer {token}"}
    requesting_response = requests.delete(f"http://127.0.0.1:8000/api/deleteProduct/{pk}", headers = headers)
    if requesting_response.status_code != 200:
        if requesting_response.status_code == 401:
            return redirect('/api/home/')
        return render( 
               request,
               'listProduct.html',
               {
                'massage': "Product Not deleted!!",
                'error': True
               }
            )
    return redirect('/api/listproduct/?page=1')

def render_product_page(request, pk, headers):
        requesting_response = requests.get(f"http://127.0.0.1:8000/api/productDetail/{pk}", headers = headers)
        if requesting_response.status_code == 200:
            response_in_json = requesting_response.json()
            return render(request, 'updateProduct.html', {'product':response_in_json})
        else:
            return redirect('/api/admin_options/')


def update_Product(request, pk):
    token = request.session.get('access_token')
    if not token:
        return redirect('/api/home/')
    headers = {'Authorization': f"Bearer {token}"}

    if request.method == 'GET':
        return render_product_page(request, pk, headers)
        
    if request.method == 'POST':
        data={
            'product_name': request.POST.get('product_name'),
            'product_description': request.POST.get('product_description'),
            'price': request.POST.get('price')}
        files = {
                'product_image': request.FILES.get('product_image')}
        
        if not files['product_image'] or not data['price'] or not data['product_name'] or not data['product_description']:
            requesting_response = requests.patch(f"http://127.0.0.1:8000/api/updateProduct/{pk}", data = data, files = files, headers = headers)
        else:
            requesting_response = requests.put(f"http://127.0.0.1:8000/api/updateProduct/{pk}", data = data, files = files, headers = headers)

        if requesting_response.status_code != 200:
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
            return render(request, 'updateProduct.html', {'massage': f"Product Not updated!!.", 'error': True})      
        return redirect('/api/listproduct/?page=1')
            
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
            requesting_response = requests.post(f"http://127.0.0.1:8000/api/addProduct/", data = data, files = files, headers = headers)
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
        if not token:
            return redirect('/api/home/')
        headers = {'Authorization': f"Bearer {token}"}
        sort_order = request.GET.get('sort')
        page = request.GET.get('page')
        requesting_response = requests.get(f"http://127.0.0.1:8000/api/product/?sort_order={sort_order}&page={page}", headers = headers)
        if requesting_response.status_code != 200:
            if requesting_response.status_code == 401:
                return redirect('/api/home/')
        response_in_json = requesting_response.json()
        products = response_in_json.get('products')
        page_number = response_in_json.get('page_number')
        total_page = response_in_json.get('total_pages')
        prev, next = update_next_previous(total_page, page_number)
        return render(request, 'products_list.html', {'products': products,'next': next,
                               'prev': prev, 'page_number': page_number, 'sort': sort_order})
               
        