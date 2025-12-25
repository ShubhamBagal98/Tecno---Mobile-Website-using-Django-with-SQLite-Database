from django.contrib import admin

# Register your models here.
from .models import Product,Brand,Customer,Order


# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display=['id','name','price','brand','ram','rom']


class AdminBrand(admin.ModelAdmin):
    list_display=['name']

admin.site.register(Product,AdminProduct)
admin.site.register(Brand,AdminBrand)
admin.site.register(Customer)
admin.site.register(Order)

