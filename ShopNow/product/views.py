from django.shortcuts import render

from product.models import product

from product.serializer import productSerializer

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Import the authetications and permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from .customPermissions import CustomizeAPIPermissions

class productView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[CustomizeAPIPermissions]
    def post(self,request):
        
        if request.data:
            self.check_permissions(request)
            serialized=productSerializer(data=request.data)

            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f"Invalid data {serialized.errors} .")
        else:
            return Response("Request is empty,No data!! ")

    def get(self,request,pk=None):
        if pk is None:
            products=product.objects.all()
            serialized=productSerializer(products,many=True)
            return Response(serialized.data)
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
                return Response("Request is empty")
        else:
            return Response("pk is None")
        
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
                return Response("Request is empty")
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
            

        