from django.urls import path
from .views import signup, profile_edit, UserLoginView, UserLogoutView

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", profile_edit, name="profile_edit"),
]
