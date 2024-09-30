from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method=='GET':
             return request.user.is_superuser
        if request.method in ['POST']:
            return request.user.is_authenticated and request.user
        if request.method in ['PUT', 'PATCH', 'DELETE','OPTIONS']:
            return request.user.is_superuser

    def has_object_permission(self, request, view, obj): 
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            if request.user.is_superuser:
                return True
            return False
        return False
    
