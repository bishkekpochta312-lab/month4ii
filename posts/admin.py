from django.contrib import admin

from posts.models import Post, Tags, User
# Register your models here.

admin.site.register(Post)

admin.site.register(Tags)

admin.site.register(User)