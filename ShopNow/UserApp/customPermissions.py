from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):  #user level permissions 
               # Allow POST for authenticated users to create new records

        print("here is the check start",request.user.is_superuser,request.auth,request.user,request.method,request.user.is_authenticated)
        if request.method in ['POST','GET']:
            print("first is the check start",request.method)
            return request.user.is_authenticated and request.auth
        
        # Allow PUT, PATCH, DELETE if user is authenticated
        if request.method in ['PUT', 'PATCH', 'DELETE','OPTIONS']:
            print("Second is the check start",request.method)
            return request.user.is_authenticated


    def has_object_permission(self, request, view, obj): 
           # Debugging print statements
        print("object is the check start",request.method)
        print(f"Request User: {request.user}",request.method)
        print(f"Object Creator: {obj.created_by}",request.method)
        print(f"token: {request.auth}",request.method)
        # Allow GET, PUT, PATCH, DELETE, OPTIONS if the user created the object or is a superuser
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            print("coming in")
            return obj.created_by == request.user or request.user.is_superuser
        
        # Deny access for other methods
        return False
    
