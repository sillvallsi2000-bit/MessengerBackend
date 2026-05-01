import time

from celery import shared_task

from .models import UserModel


@shared_task
def db_change():
    user = UserModel.objects.get(email="sillvallsi0@gmail.com")
    user.is_verificate = False if user.is_verificate else True
    user.save()


@shared_task
def long_task(x, y):
    time.sleep(10)
    return x + y
