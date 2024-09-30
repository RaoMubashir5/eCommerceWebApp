from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method=='GET':
             return request.user.is_authenticated
        if request.method in ['POST']:
            if request.user.is_authenticated and request.user:
                return True
        if request.method in ['PUT', 'PATCH', 'DELETE','OPTIONS']:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj): 
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            cart_obj=obj.cart
            if (request.user.is_authenticated) and (request.user== cart_obj.user_of_cart):
                return True
        return False
    
