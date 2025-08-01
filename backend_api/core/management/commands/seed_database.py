import random
import argparse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from faker import Faker
from core.models import Category, Product, ProductImage, Review, AuctionBid, Order, OrderItem, Payment, Shipping, Cart, PlatformReview
from django.core.management.base import BaseCommand

User = get_user_model()
fake = Faker('uk_UA')

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--categories', type=int, default=5, help='Number of categories to create')
        parser.add_argument('--products', type=int, default=20, help='Number of products to create')
        parser.add_argument('--min_hits', type=int, default=10, help='Minimum number of hits (not used in this version)')
        parser.add_argument('--orders', type=int, default=10, help='Number of orders to create')
        parser.add_argument('--reviews', type=int, default=10, help='Maximum number of reviews per product')
        parser.add_argument('--favorites', type=int, default=10, help='Maximum number of favorites per user')
        parser.add_argument('--platform_reviews', type=int, default=10, help='Number of platform reviews to create')

    def handle(self, *args, **options):
        num_users = options['users']
        num_categories = options['categories']
        num_products = options['products']
        num_orders = options['orders']
        max_reviews = options['reviews']
        max_favorites = options['favorites']
        num_platform_reviews = options['platform_reviews']

        # Очищення даних
        User.objects.exclude(is_superuser=True).delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        Review.objects.all().delete()
        AuctionBid.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        Payment.objects.all().delete()
        Shipping.objects.all().delete()
        Cart.objects.all().delete()
        PlatformReview.objects.all().delete()

        # Створення користувачів
        users = []
        for _ in range(num_users):
            email = fake.email()
            while User.objects.filter(email=email).exists():
                email = fake.email()
            username = fake.first_name()
            surname = fake.last_name()
            user = User.objects.create_user(
                email=email,
                username=username,
                surname=surname,
                password='TestPassword123!',
                is_verified=True,
                is_active=True,
            )
            users.append(user)

        # Створення категорій
        categories = []
        for _ in range(num_categories):
            name = fake.word().capitalize()
            category = Category.objects.create(
                name=name
            )
            categories.append(category)

        # Створення продуктів
        products = []
        for i in range(num_products):
            sale_type = random.choice(['fixed', 'auction'])
            price = round(random.uniform(10, 1000), 2) if sale_type == 'fixed' else None
            discount_price = None
            if sale_type == 'fixed' and random.random() < 0.5:
                discount_price = round(price * random.uniform(0.7, 0.95), 2)
                if discount_price <= 0:
                    discount_price = None
            product_name = f"{fake.word().capitalize()} {fake.word().capitalize()} {i + 1}"
            product = Product.objects.create(
                vendor=random.choice(users),
                category=random.choice(categories),
                name=product_name,
                description=fake.text(max_nb_chars=200),
                sale_type=sale_type,
                price=price,
                discount_price=discount_price,
                start_price=round(random.uniform(10, 500), 2) if sale_type == 'auction' else None,
                auction_end_time=now() + timedelta(days=random.randint(1, 7)) if sale_type == 'auction' else None,
                stock=random.randint(0, 100),
                is_approved=random.choice([True, False])
            )
            products.append(product)

        # Створення зображень продуктів
        for product in products:
            for _ in range(random.randint(1, 3)):
                ProductImage.objects.create(
                    product=product,
                    user_id=product.vendor.id,
                    image_url=f"https://picsum.photos/seed/{slugify(product.name)}/300/300.jpg"
                )

        # Створення відгуків про продукти
        for product in products:
            for _ in range(random.randint(1, max_reviews)):
                Review.objects.create(
                    product=product,
                    user=random.choice(users),
                    rating=random.randint(0, 5),
                    comment=fake.text(max_nb_chars=100),
                    is_approved = random.choice([True, False])
                )

        # Створення відгуків про платформу
        review_texts = [
            "Чудова платформа, зручний інтерфейс і швидка доставка!",
            "Дуже задоволений покупками, великий вибір товарів.",
            "Легко знайти потрібний продукт, підтримка на висоті!",
            "Трохи складна навігація, але загалом все працює добре.",
            "Швидко, зручно, але хотілося б більше знижок.",
            "Відмінний сервіс, завжди приємно купувати тут!",
            "Платформа супер, але інколи бувають затримки з доставкою.",
            "Дуже подобається аукціонна система, цікаво брати участь!",
            "Зручний кошик і швидке оформлення замовлення.",
            "Чудовий досвід покупок, рекомендую всім!"
        ]
        for i in range(num_platform_reviews):
            user = random.choice(users)
            PlatformReview.objects.create(
                user=user,
                avatar=f"https://i.pravatar.cc/150?u={user.email}",
                name=user.username,
                surname=user.surname,
                city=fake.city(),
                rating=random.randint(3, 5),
                review_text=review_texts[i],
                created_at=now() - timedelta(days=random.randint(1, 30))
            )

        # Створення ставок для аукціонів
        for product in products:
            if product.sale_type == 'auction':
                for _ in range(random.randint(1, 3)):
                    AuctionBid.objects.create(
                        product=product,
                        user=random.choice(users),
                        amount=round(random.uniform(product.start_price or 10, 500), 2)
                    )

        # Створення замовлень
        for _ in range(num_orders):
            order = Order.objects.create(
                customer=random.choice(users),
                total_amount=0,
                status=random.choice(['pending', 'paid', 'shipped', 'delivered', 'cancelled'])
            )
            total = 0
            for _ in range(random.randint(1, 3)):
                product = random.choice(products)
                quantity = random.randint(1, min(product.stock, 5))
                price = product.price if product.sale_type == 'fixed' else product.start_price
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total += price * quantity
            order.total_amount = total
            order.save()

            # Додавання даних про доставку
            Shipping.objects.create(
                order=order,
                recipient_name=f"{fake.first_name()} {fake.last_name()}",
                address=fake.address(),
                city=fake.city(),
                postal_code=fake.postcode(),
                country=fake.country()
            )

            # Додавання платежів
            Payment.objects.create(
                order=order,
                user=order.customer,
                amount=order.total_amount,
                payment_method=random.choice(['paypal', 'bank_transfer']),
                status=random.choice(['pending', 'completed', 'failed'])
            )

        # Створення кошиків
        for user in users:
            for _ in range(random.randint(0, max_favorites)):
                product = random.choice(products)
                if product.stock > 0:
                    Cart.objects.create(
                        user=user,
                        product=product,
                        quantity=random.randint(1, min(product.stock, 5))
                    )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))