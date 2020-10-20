from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [

    # path('', mainapp.products, name='index'),
    path('', mainapp.HotProductTemplateView.as_view(), name='index'),

    # path('category/<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/', mainapp.ProductsListView.as_view(), name='category'),

    # path('category/<int:pk>/page/<int:page>', mainapp.products, name='page'),
    path('category/<int:pk>/page/<int:page>', mainapp.ProductsListView.as_view(), name='page'),

    # path('product/<int:pk>/', mainapp.product, name='product'),
    path('product/<int:pk>/', mainapp.ProductDetailView.as_view(), name='product'),

]