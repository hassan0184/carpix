from django.contrib import admin
from .models import User


class user_admin(admin.ModelAdmin):
    list_display=['id','username']

admin.site.register(User,user_admin)
