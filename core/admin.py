from django.contrib import admin
from .models import Group, Post, Member, Category

# Register your models here.
admin.site.register(Group)
admin.site.register(Post)
admin.site.register(Member)
admin.site.register(Category)