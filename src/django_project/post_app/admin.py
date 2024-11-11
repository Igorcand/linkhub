from django.contrib import admin
from src.django_project.post_app.models import Post

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)