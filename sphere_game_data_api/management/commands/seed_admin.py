from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create an admin user with username "admin" and password "P@ssw0rd!123"'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'P@ssw0rd!123'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Skipping creation.')
            )
            return
        
        # Create the admin user
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        
        # Create authentication token
        token, created = Token.objects.get_or_create(user=user)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user "{username}" with token: {token.key}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Login credentials: username="{username}", password="{password}"'
            )
        )
