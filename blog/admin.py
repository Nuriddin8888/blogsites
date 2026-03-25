from django.contrib import admin
from .models import Person, Blog
# Register your models here.

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['username']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'title']