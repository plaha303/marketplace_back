from django.core.management.base import BaseCommand
from core.models import User  # Імпортуємо свою модель користувача
from faker import Faker

class Command(BaseCommand):
    help = "Seeds the database with test users."

    def handle(self, *args, **options):
        faker = Faker()
        number_of_users = 50
        for _ in range(number_of_users):
            user = User.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password='testpassword123'
            )
            self.stdout.write(self.style.SUCCESS(f"Створено користувача: {user.username}"))
