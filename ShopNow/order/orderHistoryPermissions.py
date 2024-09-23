from rest_framework.permissions import BasePermission

class OrderHistoryPermissions(BasePermission):

    def has_permission(self, request, view): 
        if request.method=='GET':
             return request.user.is_authenticated

    def has_object_permission(self, request, view, obj): 
        if request.method == 'GET':
            if obj.created_by == request.user or request.user.is_superuser: 
                return True
        return False
    
