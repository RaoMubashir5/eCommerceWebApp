from django.contrib import admin
from .models import checkoutPage

# Custom admin configuration for checkoutPage
class CheckoutPageAdmin(admin.ModelAdmin):
    list_display = ('id','full_name', 'address', 'city', 'province', 'zip_code', 'country')  # Specify the fields you want to display
    search_fields = ('full_name', 'city', 'province', 'country')  # Add search functionality
    list_filter = ('province', 'country')  # Filter options in the admin list

# Register the model and the custom admin configuration
admin.site.register(checkoutPage, CheckoutPageAdmin)
