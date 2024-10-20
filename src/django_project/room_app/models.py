from django.db import models
from uuid import uuid4
from src.django_project.user_app.models import User

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.ForeignKey(User, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name