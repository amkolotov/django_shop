from django.shortcuts import render

from .models import ProductCategory, Product


def main(request):
    chairs = Product.objects.all()[:4]
    title = 'главная'
    context = {'title': title, 'chairs': chairs}
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    title = 'продукты'
    category_menu = ProductCategory.objects.all()
    context = {'title':title, 'category_menu': category_menu}
    return render(request, 'mainapp/products.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html', {'title': 'контакты'})