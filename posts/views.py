from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from posts.models import Post
from posts.forms import CommonPostForm
from django.contrib.auth.models import AnonymousUser
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

def create_post(request: HttpRequest):
    
    if request.method == 'GET':
        form = CommonPostForm()
        return render(request, "posts/create_post.html", context = {"form": form})
    
    if request.method == "POST":
        form = CommonPostForm(request.POST, files=request.FILES)
        if form.is_valid():
            user = request.user
            if user and not isinstance(user, AnonymousUser):
                Post.objects.create(
                    header=form.cleaned_data.get("header"),
                    description=form.cleaned_data.get("description"),
                    rate=form.cleaned_data.get("rate"),
                    is_published=form.cleaned_data.get("is_published"),
                    user=user,
                )
                return redirect("post_list")
            form.add_error(None, "Вы не залогинились!")
        return render(request, "posts/create_post.html", context={"form": form})