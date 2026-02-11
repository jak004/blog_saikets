from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.list_posts, name="posts"),
    path("category/<slug:slug>/", views.posts_by_category, name="posts_by_category"),
    path("tag/<slug:slug>/", views.posts_by_tag, name="posts_by_tag"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/new/", views.post_create, name="post_create"),
    path("dashboard/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("dashboard/<int:pk>/delete/", views.post_delete, name="post_delete"),
]
