# your_app/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from accounts.factories import UserFactory

class Command(BaseCommand):
    help = 'Seeds the database with user and profile data'

    def handle(self, *args, **kwargs):
        UserFactory.create_batch(5)  # This will create 100 User and Profile pairs
        self.stdout.write(self.style.SUCCESS('100 users and profiles created!'))
