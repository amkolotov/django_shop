from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='категория')
    description = models.CharField(max_length=128, blank=True, verbose_name='описание')
    is_active = models.BooleanField(default=True, verbose_name='активна')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='имя продукта')
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(max_length=128, blank=True, verbose_name='краткое описание продукта')
    description = models.TextField(blank=True, verbose_name='описание продукта')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='цена продукта')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество на складе')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @staticmethod
    def get_items(self):
        return Product.objects.filter(is_active=True).order_by('category', 'name')


class Contacts(models.Model):
    phone = models.CharField(max_length=15, verbose_name='телефон')
    email = models.EmailField(verbose_name='email')
    city = models.CharField(max_length=100, verbose_name='город')
    address = models.CharField(max_length=100, verbose_name='адрес')

    def __str__(self):
        return self.city
