from django.contrib.auth.models import BaseUserManager




class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("email must be")
        from apps.user.models import ProfileUserModel, UserSettingsModel, UserPrivatyModel

        email = self.normalize_email(email)
        user = self.model( email = email , **kwargs)
        user.set_password(password)
        user.save()
        profile= ProfileUserModel.objects.create(user = user)
        settings = UserSettingsModel.objects.create(user = user)
        privaty = UserPrivatyModel.objects.create(user = user)

        return user
