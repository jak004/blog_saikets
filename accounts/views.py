from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm

def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    return render(request, "accounts/signup.html", {"form": form})

class CoolAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CoolAuthForm

class UserLogoutView(LogoutView):
    pass

@login_required
def profile_edit(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_edit")
    return render(request, "accounts/profile_edit.html", {"form": form})
