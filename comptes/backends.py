from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailOrPhoneBackend(ModelBackend):
    """Permet la connexion avec email OU numéro de téléphone (stocké comme username)."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        # Essai 1 : username direct (= numéro de téléphone ou email utilisé comme username)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass

        # Essai 2 : champ email
        if user is None and username and '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                pass

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
