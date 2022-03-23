from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    price = models.IntegerField()
    is_new = models.BooleanField(default=False)
    thumb = models.ImageField(default='default_product.jpg', null=True)
    is_discounted = models.BooleanField(default=False)
    category = models.ForeignKey("shop.Category", on_delete=models.CASCADE, default=None)
    brand = models.ForeignKey("shop.Brand", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'shop_products'


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop_categories'


class Brand(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='brands', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop_brands'


class Slide(models.Model):
    image = models.ImageField(default='slide.jpg')


class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    total_price = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}"


class OrderProduct(models.Model):
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f"{self.product} x{self.amount}"


RATE_CHOICES = [
    (1, "1 - Trash"),
    (2, "2 - Bad"),
    (3, "3 - OK"),
    (4, "4 - Good"),
    (5, "5 - Perfect")
]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return self.user.username
