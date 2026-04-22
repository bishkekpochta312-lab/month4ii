from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from users.forms import LoginForm, RegisterForm
from .forms import UserUpdateForm
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView
from users.service import PostObjectsService

@login_required
def update_user(request):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/update_user.html", {"form": form})

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data.get("username"))
            password = form.cleaned_data.get("password")

            user.set_password(password)
            user.save()
            return redirect("home")

        return render(request, "users/register.html", {"form": form})

    form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(
                request,
                username=cleaned_data["username"],
                password=cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("home")
            form.add_error(None, "Введенный логин или пароль неверные!")
        return render(request, "users/login.html", {"form": form})

    form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    if request.user:
        logout(request)
        return redirect("home")

    else:
        raise ValueError("Вы не авторизованы!")
    

class GetProfileView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"
    service_class = PostObjectsService()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:


        posts = self.service_class.get_post(id=2)

        kwargs["posts"] = posts

        return super().get_context_data(**kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    


        # posts = Post.objects.filter(user=self.request.user)

        # status = self.request.GET.get("status")
        # rate_from_front = self.request.GET.get("rate")

        # if status:
        #     if status == "all":
        #         ...
        #     elif status == "archived":
        #         posts = posts.filter(is_published=False)
        #     else:
        #         posts = posts.filter(is_published=True)

        # if rate_from_front:
        #     rate_from_front = int(rate_from_front)
        #     posts = posts.filter(rate__gte=rate_from_front)