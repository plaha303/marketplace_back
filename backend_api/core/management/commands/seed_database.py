from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils.timezone import now, timedelta
from faker import Faker
from core.models import User, Category, Product, Order, OrderItem, Review, Favorite, ProductImage
import random

class Command(BaseCommand):
    help = "Seeds the database with test users, categories, products, orders, reviews, and favorites."

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--categories', type=int, default=5, help='Number of categories to create')
        parser.add_argument('--products', type=int, default=20, help='Number of products to create')
        parser.add_argument('--min_hits', type=int, default=10, help='Minimum number of hit products')
        parser.add_argument('--orders', type=int, default=5, help='Number of orders to create')
        parser.add_argument('--reviews', type=int, default=10, help='Number of reviews to create')
        parser.add_argument('--favorites', type=int, default=10, help='Number of favorites to create')

    def handle(self, *args, **options):
        faker = Faker()
        num_users = options['users']
        num_categories = options['categories']
        num_products = options['products']
        min_hits = options['min_hits']
        num_orders = options['orders']
        num_reviews = options['reviews']
        num_favorites = options['favorites']

        # Створення користувачів
        self.stdout.write(self.style.SUCCESS("Створюємо користувачів..."))
        users = []
        for _ in range(num_users):
            username = faker.user_name()[:50]
            surname = faker.last_name()[:50]
            email = faker.email()
            user = User.objects.create_user(
                username=username,
                surname=surname,
                email=email,
                password='testpassword123',
                is_verified=True,
                is_active=True,
                roles=['user']
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f"Створено користувача: {user.email}"))

        # Створення категорій
        self.stdout.write(self.style.SUCCESS("Створюємо категорії..."))
        categories = []
        for i in range(num_categories):
            name = faker.word().capitalize() + " Category"
            category = Category.objects.create(
                name=name,
                category_href=slugify(name),
                parent=None if i == 0 else random.choice(categories) if categories else None
            )
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f"Створено категорію: {category.name}"))

        # Створення продуктів
        self.stdout.write(self.style.SUCCESS("Створюємо продукти..."))
        sale_types = ['fixed', 'auction']
        products = []
        hit_count = 0
        for i in range(num_products):
            name = faker.word().capitalize() + " Product"
            is_hit = i < min_hits  # Перші 10 продуктів умовно хіти
            stock = random.randint(50, 100) if is_hit else random.randint(1, 50)  # Забезпечуємо stock > 0
            sale_type = random.choice(sale_types)
            product = Product.objects.create(
                vendor=random.choice(users),
                category=random.choice(categories),
                name=name,
                description=faker.text(max_nb_chars=200),
                sale_type=sale_type,
                price=random.uniform(10.0, 1000.0) if sale_type == 'fixed' else None,
                start_price=random.uniform(5.0, 500.0) if sale_type == 'auction' else None,
                auction_end_time=now() + timedelta(days=random.randint(1, 30)) if sale_type == 'auction' else None,
                stock=stock,
                product_href=slugify(name)
            )
            # Додавання робочого зображення
            image_url = "https://picsum.photos/150"  # Стабільний placeholder
            ProductImage.objects.create(
                product=product,
                image_url=image_url
            )
            self.stdout.write(self.style.SUCCESS(f"Створено зображення для продукту: {name} з URL {image_url}"))

            products.append(product)
            if is_hit:
                hit_count += 1
            self.stdout.write(self.style.SUCCESS(f"Створено продукт: {product.name} {'(Хіт продажів)' if stock > 50 else ''}"))

        # Створення замовлень
        self.stdout.write(self.style.SUCCESS("Створюємо замовлення..."))
        for _ in range(num_orders):
            customer = random.choice(users)
            # Фільтруємо продукти з достатнім запасом
            available_products = [p for p in products if p.stock > 0]
            if not available_products:
                self.stdout.write(self.style.WARNING("Немає продуктів із достатнім запасом для створення замовлення. Пропускаємо."))
                continue
            selected_products = random.sample(available_products, k=min(len(available_products), random.randint(1, 3)))
            total_amount = 0
            order = Order.objects.create(
                customer=customer,
                status='delivered',
                total_amount=0
            )
            for product in selected_products:
                quantity = random.randint(1, min(3, product.stock))
                price = product.price or product.start_price or 0
                total_amount += price * quantity
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                product.stock = max(0, product.stock - quantity)
                product.save()
            order.total_amount = total_amount
            order.save()
            self.stdout.write(self.style.SUCCESS(f"Створено замовлення #{order.id} для користувача {customer.email}"))

        # Створення відгуків
        self.stdout.write(self.style.SUCCESS("Створюємо відгуки..."))
        used_review_pairs = set()  # Для уникнення дублювання відгуків
        for _ in range(num_reviews):
            while True:
                product = random.choice(products)
                user = random.choice(users)
                pair = (user.id, product.id)
                if pair not in used_review_pairs:
                    break
            Review.objects.create(
                product=product,
                user=user,
                rating=random.randint(0, 5),
                comment=faker.text(max_nb_chars=100)
            )
            used_review_pairs.add(pair)
            self.stdout.write(self.style.SUCCESS(f"Створено відгук для продукту {product.name} від {user.email}"))

        # Створення обраного
        self.stdout.write(self.style.SUCCESS("Створюємо обране..."))
        used_favorite_pairs = set()  # Для уникнення дублювання обраного
        for _ in range(num_favorites):
            while True:
                product = random.choice(products)
                user = random.choice(users)
                pair = (user.id, product.id)
                if pair not in used_favorite_pairs:
                    break
            Favorite.objects.create(
                user=user,
                product=product
            )
            used_favorite_pairs.add(pair)
            self.stdout.write(self.style.SUCCESS(f"Додано продукт {product.name} до обраного користувача {user.email}"))

        self.stdout.write(self.style.SUCCESS(f"Заповнення бази даних завершено! Створено {hit_count} хітів продажів."))