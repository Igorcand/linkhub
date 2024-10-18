from src.django_project.user_app.models import User
from django.contrib.auth.hashers import check_password

def authenticate(email, raw_password):
    try:
        user = User.objects.get(email=email)
        return check_password(raw_password, user.password), user
    except User.DoesNotExist:
        return None, None
