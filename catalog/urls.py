from django.urls import path
from catalog.views import index, get_contacts


urlpatterns = [
    path('', index),
    path('contacts/', get_contacts),
]
