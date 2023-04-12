from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse


def generate_token():
    return get_random_string(32)

def send_activation_email(user, user_token, request):
    activation_url = f'http://{request.get_host}{reverse("accounts:activate", args=[user_token.token, user.id])}'
    send_mail(
        'Activate your account',
        f'Please click on the link to activate your account: {activation_url}',
        'noreply@example.com',
        [user.email],
        fail_silently=False
    )