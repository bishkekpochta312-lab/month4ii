from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from users.forms import LoginForm, RegisterForm
from .forms import UserUpdateForm

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