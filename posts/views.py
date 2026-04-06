from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from posts.models import Post

# Create your views here.

def hello(request):
    return HttpResponse("hello django")

def main(request):

    return render(request, "base.html")

def about(request):

    return HttpResponse("<h1>About us</h1> <a href='/'> Main </a>")

def get_posts(request):

    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    return render(request, "posts/post_view.html", context={"posts": posts})


def get_post(request, id):
    post = get_object_or_404(Post, pk=id, is_published=True)
    return render(request, "posts/post_detail.html", {"post": post})

def published_posts(request):
    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    return render(request, "posts/posts_view.html", {"posts": posts})

