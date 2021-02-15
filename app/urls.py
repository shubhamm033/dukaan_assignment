from django.contrib import admin
from django.urls import path
from rest_framework import routers
from . import views
from django.conf.urls import url, include


router = routers.SimpleRouter()
router.register('', views.SellerViewSet, basename= 'seller')
router.register('', views.BuyerViewSet, basename= 'buyer')
router.register('', views.StoreViewSet, basename= 'Store')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include(router.urls))
]
