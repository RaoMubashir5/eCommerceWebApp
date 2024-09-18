from rest_framework.permissions import BasePermission

class CustomizeAPIPermissions(BasePermission):

    def has_permission(self, request, view):  #user level permissions 
               # Allow POST for authenticated users to create new records

        print("here is the check start",request.user.is_superuser,request.auth,request.user,request.method,request.user.is_authenticated)
        if request.method in ['GET']:
            print("first is the check start",request.method)
            return request.user.is_authenticated and request.auth
        
        if request.method =='POST':
            print("it is Post body is the check start",request.method)
            if request.user.is_superuser and request.auth:
                return True
            else:
                return False

        
        # Allow PUT, PATCH, DELETE if user is authenticated
        if request.method in ['PUT', 'PATCH', 'DELETE','OPTIONS']:
            print("Second is the check start",request.method)
            if request.user.is_authenticated:
                return True


    def has_object_permission(self, request, view, obj): 
           # Debugging print statements
        print("object is the check start",request.method)
        print(f"Request User: {request.user}",request.method)
        # print(f"Object Creator: {request.user.created_by}",request.method)
        print(f"User authenticated? : {request.user.is_authenticated}",request.method)
        # Allow GET, PUT, PATCH, DELETE, OPTIONS if the user created the object or is a superuser
        if request.method == 'GET':
            if request.user.is_authenticated:
                return True
        if request.method in ['PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            print("coming in")
            return request.user.is_superuser
        
        # Deny access for other methods
        return False
    
