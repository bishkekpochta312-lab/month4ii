from django.db import models

# Create your models here.

# INSERT INTO  posts_post () ==> Post.object.create(header="fiodf", description="Mir<ir",user = 1)

# SELECT * FROM posts_post,  posts = Post.objects,all()

# SELECT * FROM posts_post WHERE header ILIKE "% AB %",   posts = Post.objects.filter(header__icontains = "ab")

class Post(models.Model):
    header = models.CharField(max_length=255)
    description = models.TextField()
    user = models.IntegerField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.header} -- {self.user}"