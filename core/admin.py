from django.contrib import admin
from .models import Group, Post, UserProfile, Category

# Register your models here.
admin.site.register(Group)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Category)