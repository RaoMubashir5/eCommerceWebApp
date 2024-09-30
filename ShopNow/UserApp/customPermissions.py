from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user.is_authenticated
        if request.method in ['PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            return request.user.is_authenticated
        
    def has_object_permission(self, request, view, obj): 
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            return obj.created_by == request.user or request.user.is_superuser
        else:
            return False
    
