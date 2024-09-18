
from rest_framework import serializers
from ...Cart.models import cartModel,addToCart


class cartSerializer(serializers.ModelSerializer):

    class Meta:
        model=cartModel
        fields='__all__'

class AddToCartSerializer(serializers.ModelSerializer):

    class Meta:
        model=addToCart
        fields='__all__'
        
    def create(self, validated_data):
        product_in_cart = validated_data.get('cart_product')
        cart = validated_data.get('cart')

        # Check if the product is already in the cart
        existing_cart_item = addToCart.objects.filter(cart=cart, cart_product=product_in_cart).first()

        if existing_cart_item:
        # Increment the quantity of the existing product in the cart
            existing_cart_item.product_quantity += 1
            existing_cart_item.save()
            return existing_cart_item
        else:
            # Create a new cart item if the product is not already in the cart
            cart_data = addToCart.objects.create(
                cart_product=product_in_cart,
                cart=cart,
                product_quantity=validated_data.get('product_quantity')
            )
            return cart_data