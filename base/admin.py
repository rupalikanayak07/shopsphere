from django.contrib import admin
from .models import *

# Register your models here.
class productAdmin(admin.ModelAdmin):
    model=product
    list_display=['id','pimages','pcategory','price']


admin.site.register(product,productAdmin)