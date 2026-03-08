import random
from typing import Any, Dict

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from apps.auth.models import CodeUserModel
from config.extra_config.email_configuration import *
from core.dataclass.dataclass import UserDataclass


class EmailService:
    @staticmethod
    def sendemail(
        to: UserDataclass, template_name: str, context: Dict[str, any], subject: str
    ):
        template = get_template(template_name)
        render = template.render(context)
        mg = EmailMultiAlternatives(
            subject=subject,
            body="Verification code",
            from_email=EMAIL_HOST_USER,
            to=[to],
        )
        mg.attach_alternative(render, "text/html")
        mg.send()

    @staticmethod
    def generation_code() -> str:
        return str(random.randint(100000, 999999))

    @staticmethod
    def sendregistrcode(user: UserDataclass):
        code: str = EmailService.generation_code()
        CodeUserModel.objects.create(user=user, code=code)
        EmailService.sendemail(
            to=user.email,
            template_name="validation_code.html",
            context={"code": code},
            subject="Code verification",
        )
