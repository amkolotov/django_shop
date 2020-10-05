from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    context = {}
    return render(request, 'basketapp/basket.html', context)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if basket:
        basket.quantity += 1
        basket.save()
    else:
        basket = Basket.objects.create(user=request.user, product=product, quantity=1)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    context = {}
    return render(request, 'basketapp/basket.html', context)

def view(request):
    pass
