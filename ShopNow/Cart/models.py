from django.db import models
from UserApp.models import Webuser
from product.models import Product
from UserApp.models import Webuser

class AddToCart(models.Model):
    cart_product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "add_product")
    cart = models.ForeignKey('CartModel', on_delete = models.CASCADE, related_name = "products_inThisCart")
    product_quantity = models.IntegerField(default = 1, null = False, blank = False)
    class Meta:
        unique_together = ('cart_product', 'cart')
    
    def __str__(self):
        return f"AddCart: {self.id}:.cart: {self.cart}..:product: s{self.cart_product} ."

class CartModel(models.Model):
    user_of_cart = models.OneToOneField(Webuser, on_delete = models.CASCADE, related_name = "Cart_with_this_user")
    cart_product = models.ManyToManyField(Product, through = AddToCart)

    def __str__(self):
        return f"Cart:{self.id}: {self.user_of_cart} ."

