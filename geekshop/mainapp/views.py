import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from basketapp.models import Basket
from .models import ProductCategory, Product, Contacts


# def get_basket(user):
#     if user.is_authenticated:
#         basket = Basket.objects.filter(user=user)
#     else:
#         basket = []
#     return basket


def get_hot_product():
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
    return random.sample(list(products), 1)[0]


def get_sample_products(hot_product):
    sample_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]
    return sample_products


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
    queryset = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:4]
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
            'category_menu': ProductCategory.objects.filter(is_active=True),
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
            queryset = Product.objects.filter(is_active=True,
                                              category__is_active=True).order_by('price')
        else:
            queryset = Product.objects.filter(category__pk=self.kwargs['pk'], is_active=True,
                                              category__is_active=True).order_by('price')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        title = 'продукты'
        category_menu = ProductCategory.objects.all()

        if self.kwargs['pk'] == 0:
            category = {
                'pk': 0,
                'name': 'все',
            }
        else:
            category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])

        context.update({
            'title': title,
            'category_menu': category_menu,
            'category': category,
        })

        return context


# def product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     sample_products = get_sample_products(product)
#     category_menu = ProductCategory.objects.all()
#
#     context = {
#         'category_menu': category_menu,
#         'product': product,
#         'sample_products': sample_products,
#         'basket': get_basket(request.user)
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
            'category_menu': ProductCategory.objects.filter(is_active=True),
        })
        return context


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
        })
        return context