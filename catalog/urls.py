from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, get_contacts, get_products

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', get_contacts, name='contacts'),
    path('products/<int:pk>', get_products, name='products'),
]
