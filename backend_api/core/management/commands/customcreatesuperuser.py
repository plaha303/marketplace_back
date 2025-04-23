from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from ...models import User


class Command(createsuperuser.Command):
    help = 'Create a superuser with role=admin'

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        # Зберігаємо email і username перед створенням
        username = options.get('username') or options.get(self.UserModel.USERNAME_FIELD)
        email = options.get('email')

        # Викликаємо батьківський метод для створення суперкористувача
        super().handle(*args, **options)

        try:
            # Спробуємо знайти користувача за email або username
            if email:
                user = User.objects.get(email=email)
            elif username:
                user = User.objects.get(username=username)
            else:
                # Як останній варіант, беремо останнього створеного суперкористувача
                user = User.objects.filter(is_superuser=True).latest('date_joined')

            user.role = 'admin'
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set role=admin for user {user.username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found'))
        except User.MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR('Multiple superusers found, please specify username or email'))