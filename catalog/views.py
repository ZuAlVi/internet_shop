from django.shortcuts import render
from catalog.models import Product, Category


# Create your views here.


def index(request):
    categories = Category.objects.all()
    context = {
        'object_list': categories,
        'title': 'Skystore - категории'
    }
    return render(request, 'catalog/index.html', context=context)


def get_contacts(request):

    context = {
        'title': 'Skystore - контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Пользователь - {name}, телефон - {phone}, сообщение - {message}')
    return render(request, 'catalog/contacts.html', context=context)


def get_products(request, pk):
    category_item = Category.objects.get(pk=pk)
    products = Product.objects.filter(category_id=pk)
    context = {
        'object_list': products,
        'title': f'Продукты категории - {category_item.category_name}'
    }
    return render(request, 'catalog/products.html', context=context)
