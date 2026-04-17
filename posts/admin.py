from django.contrib import admin

from posts.models import Post, Tags, Comment

# Register your models here.

admin.site.register(Post)

admin.site.register(Tags)

admin.site.register(Comment)


