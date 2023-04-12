from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from users_accounts.utils import generate_token


class RegistrationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=32, default=generate_token)
    created_at = models.DateTimeField(auto_now=True)

    def verify_token(self):
        validate_exp = timezone.localtime(self.created_at) > timezone.now() - timezone.timedelta(days=1)
        if validate_exp:
            return True
        return False

    def clear_token(self):
        self.token = ''