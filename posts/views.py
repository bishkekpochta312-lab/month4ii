from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from posts.models import Post, Tags, Comment
from posts.forms import PostForm, CreateCommentForm, EditPostForm, PostSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from typing import Any
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.db.models import Q
from django.views import View

def hello(request):
    return HttpResponse("hello django")

def main(request):

    return render(request, "base.html")

def about(request):

    return HttpResponse("<h1>About us</h1> <a href='/'> Main </a>")




class PostsListView(ListView):
    model = Post
    template_name = "posts/post_view.html"
    context_object_name = "posts"
    paginate_by = 6 
    def get_queryset(self):
            queryset = Post.objects.order_by("-created_at")
            query = self.request.GET.get("query")
            tag_id = self.request.GET.get("tag")
            if query:
                queryset = queryset.filter(
                    Q(header__icontains=query) |
                    Q(description__icontains=query)
                )
            if tag_id:
                queryset = queryset.filter(tags__id=tag_id)
            return queryset
    
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



class DeletePostView(LoginRequiredMixin, View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.user != request.user:
            return redirect("post_detail", pk=pk)

        post.delete()
        return redirect("post_list")


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = "posts/edit_post.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})



class CreateCommentView(LoginRequiredMixin, View):

    def post(self, request, id):
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            post = get_object_or_404(Post, id=id)

            Comment.objects.create(
                text=form.cleaned_data["text"],
                user=request.user,
                post=post
            )

        return redirect("post_detail", pk=id)

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

# def get_posts(request):
#     tag_id = request.GET.get("tag")

#     form = PostSearchForm(request.GET or None)

#     posts = Post.objects.order_by("-created_at").prefetch_related("comments")


#     if form.is_valid():
#         query = form.cleaned_data.get('query')
#         if query:
#             posts = posts.filter(
#                 Q(header__icontains=query) |
#                 Q(description__icontains=query)
#             )


#     if tag_id:
#         posts = posts.filter(tags__id=tag_id)

#     tags = Tags.objects.all()

#     return render(request, "posts/post_view.html", {
#         'form': form,
#         "posts": posts,
#         "tags": tags
#     })
