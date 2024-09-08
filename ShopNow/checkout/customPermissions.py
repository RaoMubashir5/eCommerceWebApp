from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):  #user level permissions 
               # Allow POST for authenticated users to create new records
        print("here is the check start",request.user.is_superuser,request.auth,request.user,request.method,request.user.is_authenticated)
        if request.method in ['POST','GET']:
            print("first is the check start",request.method)
            return request.user.is_authenticated and request.auth
        else:
            return False
        
   

    
