import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView

from basketapp.models import Basket
from .models import ProductCategory, Product, Contacts


# def get_basket(user):
#     if user.is_authenticated:
#         basket = Basket.objects.filter(user=user)
#     else:
#         basket = []
#     return basket

def get_categories_menu():
    if settings.LOW_CACHE:
        key = 'categories_menu'
        categories_menu = cache.get(key)
        if categories_menu is None:
            categories_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, categories_menu)
        return categories_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_product_ordered_by_price():
    if settings.LOW_CACHE:
        key = f'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()
    if not products:
        products = Product.objects.filter(is_active=False).select_related('category')
    return random.sample(list(products), 1)[0]


def get_sample_products(hot_product):
    return Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]


# def main(request):
#     products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:4]
#     title = 'главная'
#     context = {
#         'title': title,
#         'products': products,
#         'basket': get_basket(request.user)
#     }
#     return render(request, 'mainapp/index.html', context)


class MainView(ListView):
    queryset = get_products()[:4]
    context_object_name = 'products'
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'главная',
        })
        return context


# def products(request, pk=None, page=1):
#     title = 'продукты'
#     category_menu = ProductCategory.objects.all()
#     basket = get_basket(request.user)
#
#     if pk is not None:
#         if pk == 0:
#             category = {
#                 'pk': 0,
#                 'name': 'все',
#             }
#             products = Product.objects.filter(is_active=True,
#                                               category__is_active=True).order_by('price')
#         else:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             products = Product.objects.filter(category__pk=pk, is_active=True,
#                                               category__is_active=True).order_by('price')
#
#         paginator = Paginator(products, 2)
#         try:
#             products_paginator = paginator.page(page)
#         except PageNotAnInteger:
#             products_paginator = paginator.page(1)
#         except EmptyPage:
#             products_paginator = paginator.page(paginator.num_pages)
#
#         context = {
#             'title': title,
#             'category_menu': category_menu,
#             'category': category,
#             'products': products_paginator,
#             'basket': basket,
#         }
#
#         return render(request, 'mainapp/products_list.html', context)
#
#     hot_product = get_hot_product()
#     sample_products = get_sample_products(hot_product)
#
#     context = {
#         'title': title,
#         'category_menu': category_menu,
#         'hot_product': hot_product,
#         'sample_products': sample_products,
#         'basket': get_basket(request.user)
#     }
#
#     return render(request, 'mainapp/products.html', context)


class HotProductTemplateView(TemplateView):

    template_name = 'mainapp/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hot_product = get_hot_product()
        context.update({
            'title': 'продукты',
            'category_menu': get_categories_menu(),
            'hot_product': hot_product,
            'sample_products': get_sample_products(hot_product),
        })
        return context


class ProductsListView(ListView):

    context_object_name = 'products'
    paginate_by = 2
    template_name = 'mainapp/products_list.html'

    def get_queryset(self):
        if self.kwargs['pk'] == 0:
            queryset = get_product_ordered_by_price()
        else:
            queryset = get_products_in_category_ordered_by_price(self.kwargs['pk'])

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        title = 'продукты'
        category_menu = get_categories_menu()

        if self.kwargs['pk'] == 0:
            category = {
                'pk': 0,
                'name': 'все',
            }
        else:
            category = get_category(self.kwargs['pk'])

        context.update({
            'title': title,
            'category_menu': category_menu,
            'category': category,
        })

        return context


# def product(request, pk):
#     product = get_product(pk)
#     sample_products = get_sample_products(product)
#     category_menu = get_categories_menu()
#
#     context = {
#         'category_menu': category_menu,
#         'product': product,
#         'sample_products': sample_products,
#     }
#     return render(request, 'mainapp/product.html', context)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'mainapp/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sample_products': get_sample_products(self.object),
            'category_menu': get_categories_menu(),
        })
        return context

    def get_object(self, queryset=None):
        return get_product(self.kwargs['pk'])


# def contact(request):
#     title = 'контакты'
#     contacts = Contacts.objects.all()
#     basket = get_basket(request.user)
#     context = {
#         'title': title,
#         'contacts': contacts,
#         'basket': basket,
#     }
#     return render(request, 'mainapp/contact.html', context)


class ContactView(TemplateView):
    template_name = 'mainapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contacts': Contacts.objects.all(),
            'title': 'Контакты'
        })
        return context