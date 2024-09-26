from django.contrib import admin
from UserApp.models import Webuser

class customizeAdminManager(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'created_by', 'address','password']

admin.site.register(Webuser, customizeAdminManager)


