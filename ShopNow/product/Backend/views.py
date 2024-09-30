from rest_framework.views import APIView
from ..customPermissions import CustomizeAPIPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from product.models import Product
from ShopNow.allSerializers.productSerializer import ProductSerializer
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
import math

class AddProductApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def post(self, request):

            self.check_permissions(request)
            serialized = ProductSerializer(data = request.data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response(f"Invalid data {serialized.errors} .", status = status.HTTP_400_BAD_REQUEST)
            
class GetProducts(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def get(self, request):
            sort_by = request.GET.get('sort_order')
            if sort_by:
                if sort_by == 'low_to_high':
                    products = Product.objects.all().order_by('price')
                else:
                    products = Product.objects.all().order_by('-price')
            else:
                products = Product.objects.all()

            if not products.exists():
                return Response(status = status.HTTP_204_NO_CONTENT)
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

class GetProductDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]
    
    def get(self, request, pk = None):
            try:
                instance = Product.objects.filter(id = pk)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(request, instance[0])
            serialized = ProductSerializer(instance[0])
            return Response(serialized.data, status=status.HTTP_200_OK)
    
class UpdateProductApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def put(self, request,pk = None):
        instance = Product.objects.get(id = pk)
        self.check_object_permissions(request, instance)
        serialized = ProductSerializer(instance, data = request.data)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)
        serialized.save()
        return Response(serialized.data, status = status.HTTP_200_OK)
            
    def patch(self, request,pk = None):
        instance = Product.objects.get(id = pk)
        self.check_object_permissions(request, instance)
        serialized = ProductSerializer(instance, data = request.data, partial = True)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)
        serialized.save()
        return Response(serialized.data, status = status.HTTP_200_OK)

class DeleteProductApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomizeAPIPermissions]

    def delete(self, request, pk = None):
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

