from django import forms
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio","avatar","twitter","linkedin","github","website"]
        widgets = {
            "bio": forms.Textarea(attrs={"class":"form-control","rows":4}),
            "twitter": forms.URLInput(attrs={"class":"form-control"}),
            "linkedin": forms.URLInput(attrs={"class":"form-control"}),
            "github": forms.URLInput(attrs={"class":"form-control"}),
            "website": forms.URLInput(attrs={"class":"form-control"}),
        }
