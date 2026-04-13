from django.core.management.base import BaseCommand
from apps.user.models import UserModel


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for i in range(0, 100):
            UserModel.objects.create_user(
                email=f"sillvallsi{i}@gmail.com",
                username=f"olly{i}",
                password="12345678",
            )

        self.stdout.write(self.style.SUCCESS("Users created successfully"))
