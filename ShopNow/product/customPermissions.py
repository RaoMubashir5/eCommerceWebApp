from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated and request.auth
        if request.method =='POST':
            if request.user.is_superuser and request.auth:
                return True
            else:
                return False
        if request.method in ['PUT', 'PATCH', 'DELETE','OPTIONS']:
            if request.user.is_authenticated:
                return True

    def has_object_permission(self, request, view, obj): 
        if request.method == 'GET':
            if request.user.is_authenticated:
                return True
        if request.method in ['PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            return request.user.is_superuser
        return False
    
