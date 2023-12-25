from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Feedback, Post, Version


class ProductsListView(LoginRequiredMixin, ListView):
    model = Product
    login_url = 'users:login'

    # def get_queryset(self):
    #     queryset = super().get_queryset().all()
    #     if not self.request.user.is_staff:
    #         return queryset.filter(user=self.request.user)
    #     return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['version'] = Version.objects.all()
        context['title'] = 'Skystore - продукты'
        return context


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

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.user != self.request.user and not self.request.user.is_staff:
    #         raise Http404("Вы не являетесь владельцем этого товара")
    #     return self.object


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    login_url = 'users:login'

    permission_required = 'catalog.add_product'

    def get_success_url(self):
        return reverse('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, )
        else:
            context_data['formset'] = VersionFormset()
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    login_url = 'users:login'

    def get_form_class(self):
        if self.request.user.is_staff:
            return ModeratorProductForm
        else:
            return ProductForm

    def get_success_url(self):
        return reverse('catalog:index')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    login_url = 'users:login'


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
        return reverse('catalog:post', args=[self.kwargs.get('slug')])


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
