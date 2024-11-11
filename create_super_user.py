# create_superuser.py
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_project.settings')
django.setup()

User = get_user_model()

# Ajuste as credenciais do superusuário aqui
username = 'admin'
email = 'admin@example.com'
password = 'admin'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuário '{username}' criado com sucesso.")
else:
    print(f"Superusuário '{username}' já existe.")
