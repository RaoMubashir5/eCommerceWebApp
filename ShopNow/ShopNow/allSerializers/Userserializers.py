from rest_framework import serializers
from UserApp.models import Webuser
from django.core.mail import send_mail
from django.conf import settings

class WebUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = ['password'], required = True)
    confirm_password = serializers.CharField(write_only = 'confirm_password', required = True)
    class Meta:
        model = Webuser
        fields = ['id', 'username', 'email', 'address', 'password', 'confirm_password']
    
    def create(self, validated_data):
        username = validated_data['username']
        useremail = validated_data['email']
        password = validated_data['password']
        address = validated_data['address']
        user=Webuser.objects.create(username = username, email = useremail, address = address)
        user.set_password(password)
        user.save()
        user.created_by = user 
        user.save()
        email_sending_function(username, useremail)
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
             
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Your confirming password is not matching!!')
        else:
             return data
    
def email_sending_function(username, useremail):
    subject = 'Welcome to Tutlee'
    message = f'Hi {username},\n\nThank you for registering with us. We are excited to have you on board!'
    email_from = settings.DEFAULT_FROM_EMAIL  # Set the sender's email
    recipient_list = [useremail]  # Send email to the registered user's email
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(write_only = 'password', required = True)
 












