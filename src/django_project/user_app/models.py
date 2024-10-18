from django.db import models
import uuid
from django.contrib.auth.hashers import make_password

class User(models.Model):
    app_label = "user_app"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    qnt_room = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        # Usa a implementação padrão do Django para verificar a senha
        return super().check_password(raw_password)

    def set_password(self, raw_password):
        """Define a senha, armazenando-a de forma segura."""
        self.password = make_password(raw_password)
