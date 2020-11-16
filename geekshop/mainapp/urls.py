from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [

    # path('', mainapp.products, name='index'),
    path('', mainapp.HotProductTemplateView.as_view(), name='index'),

    # path('category/<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/', cache_page(3600)(mainapp.ProductsListView.as_view()), name='category'),

    # path('category/<int:pk>/page/<int:page>', mainapp.products, name='page'),
    path('category/<int:pk>/page/<int:page>', cache_page(3600)(mainapp.ProductsListView.as_view()), name='page'),

    # path('product/<int:pk>/', mainapp.product, name='product'),
    path('product/<int:pk>/', mainapp.ProductDetailView.as_view(), name='product'),

]