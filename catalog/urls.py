from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductsListView, ProductDetailView, FeedbackCreateView, PostCreateView, PostListView, \
    PostDetailView, PostUpdateView, PostDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('contacts/', FeedbackCreateView.as_view(), name='contacts'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('post/create', PostCreateView.as_view(), name='post_create'),
    path('update/<slug:slug>', PostUpdateView.as_view(), name='post_update'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>', PostDetailView.as_view(), name='post'),
    path('delete/<slug:slug>', PostDeleteView.as_view(), name='post_delete'),
]


