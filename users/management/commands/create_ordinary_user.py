"""
Create ordinary user without specific rights
"""

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='justuser@example.com',
            first_name='justuser_first',
            last_name='justuser_last',
            is_staff=False,
            is_superuser=False)
        user.set_password('12345')
        user.save()
