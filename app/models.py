from django.db import models
import enum


class CartStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class OrderStatus(enum.Enum):
    CREATED = "CREATED"
    ACCEPTED = "ACCEPTED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class UOMType(enum.Enum):
    UNITS = "UNITS"
    KG = "KG"
    LITRE = "LITRE"


class Seller(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length= 10, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)


class Store(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    address = models.TextField()
    store_id = models.CharField(max_length=255, unique=True)
    store_url = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255, unique= True)
    description = models.TextField()
    maximum_retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    qty = models.DecimalField(max_digits=255, decimal_places=2)
    uom = models.CharField(max_length=100, choices=[(tag.value, tag.value) for tag in UOMType])



class Customer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(unique=True, max_length= 10)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255)


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, choices=[(tag.value, tag.value) for tag in OrderStatus])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True)
    order_id = models.CharField(max_length= 255, unique= True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255, null=True, blank=True)
    images = models.JSONField()
    maximum_retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, choices=[(tag.value, tag.value) for tag in CartStatus])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255, null=True, blank=True)
    images = models.JSONField()
    maximum_retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)



