from django.db import models

from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    add_datetime = models.DateField(auto_now_add=True, verbose_name='время')

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    def total_quantity(self):
        _items = self.get_items_cached
        return sum([item.quantity for item in _items])

    def total_cost(self):
        _items = self.get_items_cached
        return sum([item.product_cost for item in _items])