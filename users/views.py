from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from users.forms import LoginForm, RegisterForm
from .forms import UserUpdateForm
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, UpdateView, FormView
from users.service import PostObjectsService
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy



class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update_user.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = User.objects.create(
            username=form.cleaned_data.get("username")
        )
        password = form.cleaned_data.get("password")

        user.set_password(password)
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        user = authenticate(
            self.request,
            username=cleaned_data["username"],
            password=cleaned_data["password"],
        )

        if user:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "Введенный логин или пароль неверные!")
        return self.form_invalid(form)



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

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