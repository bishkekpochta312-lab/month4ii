from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from posts.models import Post, Tags, Comment
from posts.forms import PostForm, CreateCommentForm, EditPostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from typing import Any
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView


def hello(request):
    return HttpResponse("hello django")

def main(request):

    return render(request, "base.html")

def about(request):

    return HttpResponse("<h1>About us</h1> <a href='/'> Main </a>")

def get_posts(request):
    tag_id = request.GET.get("tag")
    posts = Post.objects.order_by("-created_at").prefetch_related("comments").all()
    if tag_id:
        posts = posts.filter(tags__id=tag_id)
    tags = Tags.objects.all()
    return render(request, "posts/post_view.html", {
        "posts": posts,
        "tags": tags
    })



class PostsListView(ListView):
    model = Post
    template_name = "posts/post_view.html"
    context_object_name = "posts"
    paginate_by = 6 

def published_posts(request):
    posts = Post.objects.filter(is_published=True).order_by('-published_at')
    return render(request, "posts/post_view.html", {"posts": posts})


    
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/create_post.html"
    # fields = ["header", "description", "is_published", "image", "rate"]
    form_class = PostForm
    success_url = reverse_lazy("post_list")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)

    if post.user != request.user:
        return redirect("post_detail", id=post.id)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    return render(request, "posts/confirm_delete.html", {"post": post})



def edit_post_view(request, id):

    post = get_object_or_404(Post, id=id)
    context = {"post": post}
    if request.user != post.user:
        return redirect("post_detail", pk=post.pk)
    if request.method == "POST":
        form = EditPostForm(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            post.header = cleaned_data["header"]
            post.description = cleaned_data["description"]
            if cleaned_data.get("image"):
                post.image = cleaned_data["image"]
            post.save()
            return redirect("post_detail", pk=post.pk)
        if form.errors:
            context["error"] = form.errors

    return render(request, "posts/edit_post.html", context=context)


@login_required
def create_comment(request, id):

    if request.method == "POST":
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            if Post.objects.filter(id=id).exists():
                Comment.objects.create(
                    text=form.cleaned_data["text"], user=request.user, post_id=id
                )
                return redirect("post_detail", pk=id)
    return redirect(
        "post_detail",
        pk=id,
    )


# def get_post(request, id):
#     post = get_object_or_404(Post, pk=id, is_published=True)
#     comment = Comment.objects.filter(post=post).all()
#     return render(
#         request, "posts/post_detail.html", context={"post": post, "comment": comment}
#     )

# @login_required
# def create_post(request: HttpRequest):
    
#     if request.method == 'GET':
#         form = CommonPostForm()
#         return render(request, "posts/create_post.html", context = {"form": form})
    
#     if request.method == "POST":
#         form = CommonPostForm(request.POST, files=request.FILES)
#         if form.is_valid():
#             user = request.user
#             Post.objects.create(
#                 header=form.cleaned_data.get("header"),
#                 description=form.cleaned_data.get("description"),
#                 rate=form.cleaned_data.get("rate"),
#                 is_published=form.cleaned_data.get("is_published"),
#                 user=user,
#             )
#             return redirect("post_list")
#         messages.error(request, "Ошибка при созданий комментария")
#         return render(request, "posts/create_post.html", context={"form": form})