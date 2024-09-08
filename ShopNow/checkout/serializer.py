from rest_framework import serializers

from checkout.models import checkoutPage

class checkoutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=checkoutPage
        fields='__all__'

    #     except='checkout_user'
    
    # def create(self,validated_data):
    #     full_name=validated_data['full_name']
    #     address=validated_data['address']
    #     city=validated_data['city']
    #     province=validated_data['province']
    #     zip_code=validated_data['zip_code']
    #     country=validated_data['country']

    #     user=checkoutPage.objects.create(full_name=full_name,address=address,city=city,
    #                                      province=province,country=country,zip_code=zip_code,)
                                         
       
    #     user.save()
    #     user.created_by=user   #user.created.created_by=self.instance
    #     user.save()
    #     return user
  