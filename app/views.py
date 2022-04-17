import json


from django.http.multipartparser import MultiPartParser

import collections
from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.parsers import FormParser
from rest_framework.response import Response
from .serializers import ProductResponseSerializer, ProductResponseListSerializer
from . import serializers, utils
from .models import Seller, Store, Customer, Category, Product, Cart, CartProduct, Order, OrderProduct, CartStatus, \
    OrderStatus
import uuid
import jwt
from .authentication import *


class SellerViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def create_seller(self, request):
        serializer = serializers.CreateSellerRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        name = data.get("name")
        phone_number = data.get("phone_number")
        address = data.get("address")

        # hardcoding the jwt secret here can be stored in a diff file
        print("something new")
        jwt_secret = "abcdefgh"
        print("I am here")
        print("something new")
        seller = Seller(name=name,
                        phone_number=phone_number,
                        address=address)
        seller.save()

        token_json = {
            "_id": phone_number
        }
        token = jwt.encode(token_json, jwt_secret, algorithm="HS256")

        return Response(data=token, status=status.HTTP_200_OK)

class StoreViewSet(viewsets.ViewSet):
    authentication_classes = [JWTTokenAuthentication]


    @action(detail=False, methods=['post'])
    def create_store(self, request):
        serializer = serializers.CreateStoreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        seller = Seller.objects.all().first()
        # get from token

        store_name = data.get("store_name")
        store_address = data.get("store_address")

        # This prefix can be stored at some other place too like a common file
        prefix = "https://dukaan.com/"
        store_id = store_name.split(" ")[0] + uuid.uuid4().hex[:5]
        store_url = prefix + store_id

        store = Store(seller=seller,
                      store_url=store_url,
                      store_id=store_id,
                      address=store_address,
                      name=store_name
                      )

        store.save()
        response_data = {"store_id": store_id, "store_url": store_url}

        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_product(self, request):
        parser_classes = (FormParser, MultiPartParser)
        serializer_data = dict()

        serializer_data.update(json.loads(request.data['data']))
        serializer = serializers.CreateProductRequestSerializer(data=serializer_data)

        serializer.is_valid(raise_exception=True)
        data = serializer.data

        file = request.data['file']
        image_url = utils.save_image_and_generate_url(file)
        image_url_data = {"image_url_list": image_url}

        product_name = data.get("product_name")
        product_description = data.get("product_description")
        maximum_retail_price = data.get("maximum_retail_price")
        sale_price = data.get("sale_price")
        category_name = data.get("category")
        store_id = data.get("store_id")
        qty = data.get("qty")
        uom = data.get("uom")

        category = Category.objects.filter(name=category_name).first()
        store = Store.objects.filter(store_id=store_id).first()

        if category is None:
            category = Category(name=category_name)
            category.save()

        product_id = uuid.uuid4().hex[:10]
        # //  This can also be created by some other way.

        product = Product(category=category,
                          store=store,
                          name=product_name,
                          description=product_description,
                          maximum_retail_price=maximum_retail_price,
                          sale_price=sale_price,
                          qty=qty,
                          uom=uom,
                          images=image_url_data,
                          product_id=product_id
                          )
        product.save()

        response_data = {"product_id": product_id,
                         "image_url": image_url_data,
                         "name": product_name}

        return Response(data=response_data, status=status.HTTP_200_OK)


class BuyerViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_store_details(self, request):
        store_url = request.query_params.get('store_url')
        store = Store.objects.filter(store_url=store_url).first()

        if store is None:
            return Response(status=status.HTTP_204_NO_CONTENT)


        response_data = {"store_id": store.store_id,
                         "store_address": store.address,
                         "store_name": store.name}

        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_store_products(self, request):
        store_url = request.query_params.get('store_url')

        result = Product.objects.filter(store__store_url = store_url).all().select_related("category")

        if len(result) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        product_map = collections.defaultdict(list)

        for product in result:
            product_map[product.category.name].append(product)

        product_map = sorted(product_map.items(), key = lambda  x: len(x[1]))
        ans_map = collections.OrderedDict()
        ans_list = []

        for product in product_map:
            temp_product_map =  collections.OrderedDict()
            temp_product_map["category"] = product[0]
            temp_product_map["products"] = product[1]
            ans_list.append(temp_product_map)
        ans_map.update({"response": ans_list})
        response_serializer = ProductResponseListSerializer(instance= ans_map)

        return Response(data = response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def add_item_to_cart(self, request):
        serializer = serializers.AddItemToCartRequestSerialzer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        product_id = data.get("product_id")
        store_url = data.get("store_url")
        qty = data.get("qty")
        cart_id = data.get("cart_id")
        print(type(qty))
        cart = Cart.objects.filter(id = cart_id).first()
        product = Product.objects.filter(product_id=product_id).first()
        store = Store.objects.filter(store_url=store_url).first()

        if cart_id is None:
            cart = Cart(store=store,
                        status=CartStatus.ACTIVE.value)
            cart.save()

        cart_product = CartProduct(
            product_id=product_id,
            product_name=product.name,
            product_description=product.description,
            images=product.images,
            maximum_retail_price=product.maximum_retail_price,
            category=product.category,
            sale_price=product.sale_price,
            cart=cart,
            qty=qty)

        cart_product.save()

        response_data = {"cart_id": cart.id,
                         "product_id": product_id,
                         "store_url": store_url
                         }

        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_item_from_cart(self, request):

        serializer = serializers.RemoveItemCartRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        product_id = data.get("product_id")
        qty = data.get("qty")
        cart_id = data.get("cart_id")

        cart_product = CartProduct.objects.filter(product_id=product_id,
                                                  cart__id=cart_id).first()

        # here we can add scenarios like based on qty difference same produuct coming again etc

        if cart_product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_product.delete()

        return Response(data = product_id, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_order(self, request):

        serializer = serializers.CreateOrderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        # passing the cart id in this case, if we use some other db
        # like MONGODB or REDIS, then we will pass the whole cart object

        cart_id = data.get("cart_id")
        customer_phone_number = data.get("customer_phone_no")

        customer = Customer.objects.filter(phone_number=customer_phone_number).first()

        if customer is None:
            customer = Customer(phone_number=customer_phone_number)
            customer.save()

        cart = Cart.objects.prefetch_related('cartproduct_set').filter(id=cart_id).first()

        order_id = uuid.uuid4().hex[:10]

        order = Order(store = cart.store,
                      order_id=order_id,
                      customer=customer,
                      status=OrderStatus.CREATED.value
                      )
        order.save()

        orderproducts = list()
        for cart_product in cart.cartproduct_set.all():
            orderProduct = OrderProduct(product_id=cart_product.product_id,
                                        product_name=cart_product.product_name,
                                        product_description=cart_product.product_description,
                                        images=cart_product.images,
                                        maximum_retail_price=cart_product.maximum_retail_price,
                                        category=cart_product.category,
                                        sale_price=cart_product.sale_price,
                                        order=order,
                                        qty=cart_product.qty)
            orderproducts.append(orderProduct)
        OrderProduct.objects.bulk_create(orderproducts)

        return Response(data=order_id, status=status.HTTP_200_OK)
