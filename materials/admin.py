from django.contrib import admin
from .models import Material,Product,UserProduct,Trashcan

admin.site.register(Material)
admin.site.register(Product)
admin.site.register(UserProduct)
admin.site.register(Trashcan)
