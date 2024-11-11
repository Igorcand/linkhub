from django.contrib import admin
from src.django_project.user_app.models import User

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)