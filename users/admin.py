from django.contrib import admin
from .models import User,Profile


class user_admin(admin.ModelAdmin):
    list_display=['id','username']

admin.site.register(User,user_admin)
admin.site.register(Profile)
