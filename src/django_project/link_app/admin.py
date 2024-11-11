from django.contrib import admin
from src.django_project.link_app.models import Link

class LinkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Link, LinkAdmin)