from django.db import models

# Create your models here.

# INSERT INTO  posts_post () ==> Post.object.create(header="fiodf", description="Mir<ir",user = 1)

# SELECT * FROM posts_post,  posts = Post.objects,all()

# SELECT * FROM posts_post WHERE header ILIKE "% AB %",   posts = Post.objects.filter(header__icontains = "ab")

class User(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    age = models.PositiveIntegerField()

class Tags(models.Model):
    title = models.CharField(max_length=255)

class Post(models.Model):

    header = models.CharField(max_length=255)
    description = models.TextField()
    rate = models.IntegerField(null=True, blank=True)

    tags = models.ManyToManyField(Tags,blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=255, default="Untitled Post")
    content = models.TextField(default="")
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="posts", null=True, blank=True)


    def __str__(self):
        return f"{self.header}"