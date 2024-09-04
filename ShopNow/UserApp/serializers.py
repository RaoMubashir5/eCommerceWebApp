import rest_framework
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer #it is to convert the python dictionry into json as in api only json reponse will be sent.
from UserApp.models import Webuser

# ...........................validator().............................
# def checkFirstLetter(value):
#     if not value[0].isupper():
#         raise serializers.ValidationError("country name's first letter should be capital")
#     else:
#         return value


class WebUserSerializer(serializers.ModelSerializer):
     #do not need to declare the fields
    password=serializers.CharField( write_only=['password'],required=True)
    confirm_password=serializers.CharField( write_only='confirm_password',required=True)

    class Meta:
        model=Webuser
        fields=['username','email','password','confirm_password']
    
    def create(self,validated_data):
        username=validated_data['username']
        useremail=validated_data['email']
        password=validated_data['password']

        user=Webuser.objects.create(username=username,email=useremail)
        user.set_password(password)
        user.save()
        user.created_by=user   #user.created.created_by=self.instance
        user.save()
        return user
    
    def update(self,instance,validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.email=validated_data.get('email',instance.email)
      
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
             
        
    
    # def update(self,instance,validated_data):
      

    def validate_username(self,value):
            if  value.lower():
                return value.capitalize() 
            else:
                 return value.capitalize() 
             

            # .............................validate(self,data).................................
            # There are the validations for an object that there would be multiple fields to validate, when the serialized.is_valid() function is called.
    def validate(self,data):
        if data.get('password')!=data.get('confirm_password'):
            raise serializers.ValidationError('Your confirming password is not matching!!')
        else:
             return data


    
class loginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only='password', required=True)
    #it is not associated to any model, its just for the validation and conversion












