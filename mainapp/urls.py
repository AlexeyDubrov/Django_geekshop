from django.urls import path, re_path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('products/', mainapp.products, name='products'),
    re_path(r'^category/(?P<pk>\d+)/products/$', mainapp.catalog, name='catalog'),
    re_path(r'^category/(?P<pk>\d+)/products/page/(?P<page>\d+)/$', mainapp.catalog, name='catalog_page'),
    re_path(r'^product/(?P<pk>\d+)/$', mainapp.product_page, name='product_page'),

    path('contact/', mainapp.contact, name='contact'),
]
