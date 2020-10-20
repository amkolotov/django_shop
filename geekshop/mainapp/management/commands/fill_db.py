import json
import os

from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, Contacts

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json')) as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()

        for category in categories:
            ProductCategory.objects.create(**category)

        products = load_from_json('products')
        Product.objects.all().delete()

        for product in products:
            category_name = product["category"]
            _category = ProductCategory.objects.get(name=category_name)
            product["category"] = _category
            new_product = Product.objects.create(**product)

        contacts = load_from_json('contact__locations')
        Contacts.objects.all().delete()

        for contact in contacts:
            Contacts.objects.create(**contact)

        super_user = ShopUser.objects.create_superuser('django', '', 'geekshop', age=33)
