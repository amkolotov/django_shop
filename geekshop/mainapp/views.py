import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import ProductCategory, Product


def get_basket(user):
    if user.is_authenticated:
        basket = Basket.objects.filter(user=user)
    else:
        basket = []
    return basket


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_sample_products(hot_product):
    sample_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return sample_products


def main(request):
    products = Product.objects.all()[:4]
    title = 'главная'
    context = {
        'title': title,
        'products': products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    title = 'продукты'
    category_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category=category).order_by('price')

        context = {
            'title':title,
            'category_menu': category_menu,
            'category': category,
            'products': products,
            'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', context)

    hot_product = get_hot_product()
    sample_products = get_sample_products(hot_product)

    context = {
        'title': title,
        'category_menu': category_menu,
        'hot_product': hot_product,
        'sample_products': sample_products,
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/products.html', context)

def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sample_products = get_sample_products(product)
    category_menu = ProductCategory.objects.all()

    context = {
        'category_menu': category_menu,
        'product': product,
        'sample_products': sample_products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', context)




def contact(request):
    return render(request, 'mainapp/contact.html', {'title': 'контакты', 'basket': get_basket(request.user)})