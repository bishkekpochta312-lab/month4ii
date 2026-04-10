from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

# INSERT INTO  posts_post () ==> Post.object.create(header="fiodf", description="Mir<ir",user = 1)

# SELECT * FROM posts_post,  posts = Post.objects,all()

# SELECT * FROM posts_post WHERE header ILIKE "% AB %",   posts = Post.objects.filter(header__icontains = "ab")




# class User(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(default="mirdins@bk.ru")
#     created_at = models.DateTimeField(default=timezone.now)  # дата регистрации

#     def __str__(self):
#         return self.name
    
class Tags(models.Model):
    title = models.CharField(max_length=255)

class Post(models.Model):

    header = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    rate = models.IntegerField(null=True, blank=True)

    tags = models.ManyToManyField(Tags,blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  

    title = models.CharField(max_length=255, default="Untitled Post", blank=True)
    content = models.TextField(default="", blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="posts", null=True, blank=True)


    def __str__(self):
        return f"{self.header}"