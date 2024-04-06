from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ( 'first_name', 'email', 'username', 'phone_number', 'dob', 'uuid',)
admin.site.register(User, UserAdmin)
