"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts.views import (
    PostCreateView,
    PostDetailView,
    PostsListView,
    about,
    create_comment,
    delete_post,
    edit_post_view,
    hello,
    main,
)
from django.conf import settings
from django.conf.urls.static import static
from posts.views import published_posts
from users.views import login_view, logout_view, register_view, update_user, GetProfileView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('', main, name='home'),
    path('about/',about),
    path("posts/", PostsListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
        path("posts/", published_posts, name="posts"),
    path("users/register/", register_view, name="register"),
    path("users/login/", login_view, name="login"),
    path("users/logout/", logout_view, name="logout"),
    path("post/<int:id>/delete/", delete_post, name="delete_post"),
    path("post/<int:id>/edit/", edit_post_view, name="edit_post"),
    path("post/<int:id>/comment/", create_comment, name="create_comment"),
    path("profile/edit/", update_user, name="update_user"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)