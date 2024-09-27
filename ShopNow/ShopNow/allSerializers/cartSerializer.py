
from rest_framework import serializers
from Cart.models import CartModel
from Cart.models import AddToCart

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model=CartModel
        fields='__all__'

class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model=AddToCart
        fields='__all__'
        
    def create(self, validated_data):
        product_in_cart = validated_data.get('cart_product')
        cart = validated_data.get('cart')
        existing_cart_item = AddToCart.objects.filter(cart = cart, cart_product = product_in_cart).first()
        # if existing_cart_item:
        #     existing_cart_item.product_quantity += 1
        #     existing_cart_item.save()
        #     return existing_cart_item
        cart_data = AddToCart.objects.create(
                cart_product = product_in_cart,
                cart = cart,
                product_quantity = validated_data.get('product_quantity')
            )
        return cart_data