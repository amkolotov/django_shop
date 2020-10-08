from django.db import models

from geekshop import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    add_datetime = models.DateField(auto_now_add=True, verbose_name='время')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _products = Basket.objects.filter(user=self.user)
        _total_quantity = sum([product.quantity for product in _products])
        return _total_quantity

    @property
    def total_cost(self):
        _products = Basket.objects.filter(user=self.user)
        _total_cost = sum([product.product_cost for product in _products])
        return _total_cost