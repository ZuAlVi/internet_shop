from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductsListView, ProductDetailView, FeedbackCreateView, PostCreateView, PostListView, \
    PostDetailView, PostUpdateView, PostDeleteView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('categories', CategoryListView.as_view(), name='categories'),
    path('contacts/', FeedbackCreateView.as_view(), name='contacts'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('product/create', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
    path('post/create', PostCreateView.as_view(), name='post_create'),
    path('update/<slug:slug>', PostUpdateView.as_view(), name='post_update'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>', PostDetailView.as_view(), name='post'),
    path('delete/<slug:slug>', PostDeleteView.as_view(), name='post_delete'),
]


