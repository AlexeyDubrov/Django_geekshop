import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from mainapp.models import ProductCategory, Product


def get_hot_product():
    # products = Product.objects.all()
    products_id = Product.objects.values_list('id', flat=True)
    hot_product_id = random.choice(products_id)
    return Product.objects.get(pk=hot_product_id)


def related_products(product):
    return Product.objects.filter(category=product.category).exclude(id=product.id)


def index(request):
    context = {
        'page_title': 'главная',
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    hot_product = get_hot_product()
    _related_products = related_products(hot_product)

    context = {
        'page_title': 'каталог',
        'hot_product': hot_product,
        'related_products': _related_products,
    }
    return render(request, 'mainapp/products.html', context)


def product_page(request, pk):
    context = {
        'page_title': 'продукт',
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product_page.html', context)


def catalog(request, pk, page=1):
    if int(pk) == 0:
        category = {'pk': 0, 'name': 'Все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(category=category)

    products_paginator = Paginator(products, 2)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'каталог',
        'category': category,
        'products': products,
    }
    return render(request, 'mainapp/catalog.html', context)


def contact(request):
    locations = [
        {
            'city': 'Москва',
            'phone': '+7-123-45-6789',
            'email': 'master@master.ru',
            'address': 'Москва, ул. Тверская, 15,'
        },
        {
            'city': 'Ростов-на-Дону',
            'phone': '+7-987-65-4321',
            'email': 'master@master.ru',
            'address': 'Ростов-на-Дону, ул Горького, 100',
        },
        {
            'city': 'Иркутск',
            'phone': '+7-112-445-6677',
            'email': 'master@master.ru',
            'address': 'Иркутск, бульвар Гагарина, 21',
        }
    ]

    context = {
        'page_title': 'контакты',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', context)
