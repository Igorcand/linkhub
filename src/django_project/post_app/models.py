from django.db import models
from uuid import uuid4
from src.django_project.user_app.models import User
from src.django_project.room_app.models import Room
from src.django_project.link_app.models import Link


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=1024)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    links = models.ManyToManyField(Link, blank=True)



    def __str__(self):
        return self.title