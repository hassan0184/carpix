from django.contrib import admin
from .models import Location,Booth,Camera

class location_admin(admin.ModelAdmin):
    list_display=['id','name']

class booth_admin(admin.ModelAdmin):
    list_display=['id','name','location']

class camera_admin(admin.ModelAdmin):
    list_display=['id','name','status','location','booth']

admin.site.register(Location,location_admin)
admin.site.register(Booth,booth_admin)
admin.site.register(Camera,camera_admin)
