from django.contrib import admin

from mainapp.models import Product, ProductCategory

admin.site.register(ProductCategory)
admin.site.register(Product)
