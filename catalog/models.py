from django.db import connection
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {
    'blank': True,
    'null': True,
}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')


class Product(models.Model):
    product_name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='product/', verbose_name='Превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    date_make = models.DateTimeField(auto_now=True, verbose_name='Дата создания', **NULLABLE)
    date_changed = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения', **NULLABLE)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('product_name',)


class Feedback(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'Пользователь - {self.user_name}, телефон - {self.phone}, сообщение - {self.message}'

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(unique=True, max_length=150, verbose_name='slag', **NULLABLE)
    text = models.TextField(verbose_name='Содержимое')
    photo = models.ImageField(upload_to='post/', verbose_name='Превью', **NULLABLE)
    make_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return f'Пост - {self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    number = models.CharField(max_length=100, verbose_name='номер версии')
    name = models.TextField(max_length=150, verbose_name='название версии')
    current_version = models.BooleanField(default=False, verbose_name='текущая версия')

    def __str__(self):
        return f'Продукт {self.product} версии {self.number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


@receiver(post_save, sender=Version)
def set_current_version(sender, instance, **kwargs):
    if instance.current_version:
        Version.objects.filter(product=instance.product).exclude(pk=instance.pk).update(current_version=False)
