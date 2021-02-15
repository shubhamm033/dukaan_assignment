import json

from rest_framework import serializers


class CreateSellerRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    def validate(self, data):
        data = dict(data)

         # No external validation is put

        return data


class CreateStoreRequestSerializer(serializers.Serializer):
    store_name = serializers.CharField()
    store_address = serializers.CharField()

    def validate(self, data):
        data = dict(data)

         # No external validation is put

        return data



class CreateProductRequestSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_description = serializers.CharField()
    maximum_retail_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.CharField()
    qty = serializers.DecimalField(max_digits=10, decimal_places=2)
    uom = serializers.CharField()
    store_id = serializers.CharField()


    def validate(self, data):
        data = dict(data)
        return data



class AddItemToCartRequestSerialzer(serializers.Serializer):
    cart_id = serializers.IntegerField(allow_null=True, required=False)
    product_id = serializers.CharField()
    qty = serializers.DecimalField(max_digits=10, decimal_places=2)
    store_url = serializers.CharField()

    def validate(self, data):
        data = dict(data)

         # No external validation is put

        return data


class RemoveItemCartRequestSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    product_id = serializers.CharField()
    qty = serializers.DecimalField(max_digits=10, decimal_places=2)
    store_url = serializers.CharField()

    def validate(self, data):
        data = dict(data)

         # No external validation is put

        return data



class CreateOrderRequestSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    customer_phone_no = serializers.CharField()

    def validate(self, data):
        data = dict(data)

         # No external validation is put

        return data

class ProductDetailsResponseSerialzer(serializers.Serializer):
    name = serializers.CharField()
    product_id = serializers.CharField()
    description = serializers.CharField()
    maximum_retail_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    images = serializers.JSONField()
    qty = serializers.DecimalField(max_digits=255, decimal_places=2)
    uom = serializers.CharField()

    def to_representation(self, instance):
        print(instance)
        return super().to_representation(instance)

class ProductResponseSerializer(serializers.Serializer):
    category = serializers.CharField()
    products = serializers.ListField(child=ProductDetailsResponseSerialzer())

    def to_representation(self, instance):
        return super().to_representation(instance)


class ProductResponseListSerializer(serializers.Serializer):
    response = serializers.ListField(child=ProductResponseSerializer())

    def to_representation(self, instance):
        return super().to_representation(instance)






