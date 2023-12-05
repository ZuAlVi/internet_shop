from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Feedback, Post
from pytils.translit import slugify


class ProductsListView(ListView):
    model = Product
    extra_context = {
        'title': 'Skystore - продукты'
    }


class ProductDetailView(DetailView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs.get('pk'))
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Продукт - {product.product_name}'

        return context_data


class FeedbackCreateView(CreateView):
    model = Feedback
    fields = ('user_name', 'phone', 'message')
    extra_context = {
        'title': 'Skystore - контакты'
    }
    success_url = reverse_lazy('catalog:contacts')


class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'text', 'photo')
    success_url = reverse_lazy('catalog:post_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'text', 'photo')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:post', args=self.kwargs.get('slug'))


class PostListView(ListView):
    model = Post
    extra_context = {
        'title': 'Skystore - все посты'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('catalog:post_list')
