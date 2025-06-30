import random
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from faker import Faker
from store.models import Category, Product, ProductImage, Review, AuctionBid, Order, OrderItem, Payment, Shipping, Cart

User = get_user_model()
fake = Faker('uk_UA')

def seed_database():
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

    # Створення користувачів
    users = []
    for _ in range(10):
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
    for _ in range(5):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            category_href=slugify(fake.word())
        )
        categories.append(category)

    # Створення продуктів
    products = []
    for _ in range(20):
        sale_type = random.choice(['fixed', 'auction'])
        price = round(random.uniform(10, 1000), 2) if sale_type == 'fixed' else None
        discount_price = None
        if sale_type == 'fixed' and random.choice([True, False]):
            discount_price = round(price * random.uniform(0.7, 0.95), 2)  # Знижка 5-30%
        product = Product.objects.create(
            vendor=random.choice(users),
            category=random.choice(categories),
            name=fake.word().capitalize(),
            description=fake.text(max_nb_chars=200),
            sale_type=sale_type,
            price=price,
            discount_price=discount_price,
            start_price=round(random.uniform(10, 500), 2) if sale_type == 'auction' else None,
            auction_end_time=now() + timedelta(days=random.randint(1, 7)) if sale_type == 'auction' else None,
            stock=random.randint(0, 100),
        )
        products.append(product)

    # Створення зображень продуктів
    for product in products:
        for _ in range(random.randint(1, 3)):
            ProductImage.objects.create(
                product=product,
                user_id=product.vendor.id,
                image_url=f"https://example.com/images/{slugify(product.name)}.jpg"
            )

    # Створення відгуків
    for product in products:
        for _ in range(random.randint(0, 5)):
            Review.objects.create(
                product=product,
                user=random.choice(users),
                rating=random.randint(0, 5),
                comment=fake.text(max_nb_chars=100)
            )

    # Створення ставок для аукціонів
    for product in products:
        if product.sale_type == 'auction':
            for _ in range(random.randint(0, 5)):
                AuctionBid.objects.create(
                    product=product,
                    user=random.choice(users),
                    amount=round(random.uniform(product.start_price or 10, (product.start_price or 10) * 2), 2)
                )

    # Створення замовлень
    for _ in range(10):
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
        for _ in range(random.randint(0, 3)):
            product = random.choice(products)
            if product.stock > 0:
                Cart.objects.create(
                    user=user,
                    product=product,
                    quantity=random.randint(1, min(product.stock, 5))
                )

    print("Database seeded successfully!")