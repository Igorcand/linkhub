from django.contrib import admin
from src.django_project.room_app.models import Room

class RoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(Room, RoomAdmin)