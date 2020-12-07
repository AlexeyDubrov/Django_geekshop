import os
import json

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.conf import settings


def load_from_json(file_name):
    with open(
            os.path.join(settings.JSON_PATH, f'{file_name}.json'),
            encoding='utf-8'
    ) as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        [ProductCategory.objects.create(**category) for category in categories]

        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            # Получаем категорию по имени
            # _category = ProductCategory.objects.get(name=category_name)
            # _category = ProductCategory.objects.filter(name=category_name).first()
            # _category = list(ProductCategory.objects.filter(name=category_name))[0]
            _category = ProductCategory.objects.get(name=category_name)  # .get() -> concrete object
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        # if not len(ShopUser.objects.filter(username='django'))
        # if ShopUser.objects.filter(username='django').count() == 0:
        if not ShopUser.objects.filter(username='django').exists():
            # ShopUser.objects.create(username='django', email='admin@geekshop.local', password='geekbrains')
            ShopUser.objects.create_superuser(username='django', email='admin@geekshop.local', password='geekbrains')

# 7 min -> 20:06 AIR
