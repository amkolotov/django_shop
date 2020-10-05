from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import ProductCategory, Product


def main(request):
    chairs = Product.objects.all()[:4]
    title = 'главная'
    context = {'title': title, 'chairs': chairs}
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    title = 'продукты'
    category_menu = ProductCategory.objects.all()

    basket = []
    basket_quantity = {'quantity': 0, 'cost': 0}
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        for added_product in basket:
            basket_quantity['quantity'] += added_product.quantity
            basket_quantity['cost'] += added_product.product.price * added_product.quantity

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
            'basket_quantity': basket_quantity,
        }

        return render(request, 'mainapp/products_list.html', context)

    same_products = Product.objects.all()[3:5]

    context = {
        'title': title,
        'category_menu': category_menu,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html', {'title': 'контакты'})