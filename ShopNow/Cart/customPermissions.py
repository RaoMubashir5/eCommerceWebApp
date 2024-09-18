from rest_framework.permissions import BasePermission
from .models import cartModel

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):  #user level permissions 
               # Allow POST for authenticated users to create new records

        print("here is the check start",request.user.is_superuser,request.auth,request.user,request.method,request.user.is_authenticated)
        if request.method=='GET':
             return request.user.is_authenticated
        
        if request.method in ['POST']:
            # cart_obj=cartModel.objects.get(id=int(request.data.get('cart'))) 
            # print("first is the check start",request.method,request.user,cart_obj.user_of_cart)

            if request.user.is_authenticated and request.user:
                print("User to  sahi ha")
                return True
        
        # Allow PUT, PATCH, DELETE if user is authenticated
        if request.method in ['PUT', 'PATCH', 'DELETE','OPTIONS']:
            print("Second is the check start",request.method)
            return request.user.is_authenticated


    def has_object_permission(self, request, view, obj): 
           # Debugging print statements
        print("object is the check start",request.method)
        print(f"Request User: {request.user}",request.method)
        # print(f"Object Creator: {request.user.created_by}",request.method)
        # print(f"token: {request.auth}",request.method)
        # Allow GET, PUT, PATCH, DELETE, OPTIONS if the user created the object or is a superuser
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            cart_obj=obj.cart
            if (request.user.is_authenticated) and (request.user== cart_obj.user_of_cart):
                print(f"User to  sahi ha{cart_obj}")
                return True
        
        # Deny access for other methods
        return False
    
