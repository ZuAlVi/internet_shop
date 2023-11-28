from django.core.management import BaseCommand, call_command
from django.db import ProgrammingError, IntegrityError
from catalog.models import Category


class Command(BaseCommand):
    requires_migrations_check = True

    def handle(self, *args, **options):

        fixtures_path = 'data.json'

        Category.objects.all().delete()
        Category.truncate_table_restart_id()

        try:
            call_command('loaddata', fixtures_path)
        except ProgrammingError:
            pass
        except IntegrityError as e:
            self.stdout.write(f'Invalid fixture: {e}', self.style.NOTICE)
        else:
            self.stdout.write('Command have been completed successfully', self.style.SUCCESS)



        # category_list = [
        #     {'category_name': 'Auto'},
        #     {'category_name': 'Fruits'},
        #     {'category_name': 'Sport'},
        # ]

        # auto = Category(category_name='Auto').save()
        # fruits = Category(category_name='Fruits').save()
        # sport = Category(category_name='Sport').save()


        # product_list = [
        #     {
        #         'product_name': 'Suzuki',
        #         'category': auto,
        #         'price': 500000,
        #     },
        #     {
        #         'product_name': 'apple',
        #         'category': fruits,
        #         'price': 20,
        #     },
        #     {
        #         'product_name': 'Ball',
        #         'category': sport,
        #         'price': '500',
        #     }
        # ]

        # category_for_create = []
        #
        # for category_item in category_list:
        #     category_for_create.append(Category(**category_item))
        #
        # Category.objects.bulk_create(category_for_create)

        # product_for_create = []
        #
        # for product_item in product_list:
        #     product_for_create.append(Product(**product_item))
        #
        # Product.objects.bulk_create(product_for_create)
