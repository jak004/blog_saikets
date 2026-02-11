from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","excerpt","content","cover_image","category","tags","status","featured"]
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "excerpt": forms.TextInput(attrs={"class":"form-control"}),
            "category": forms.Select(attrs={"class":"form-select"}),
            "tags": forms.SelectMultiple(attrs={"class":"form-select"}),
            "status": forms.Select(attrs={"class":"form-select"}),
            "featured": forms.CheckboxInput(attrs={"class":"form-check-input"}),
        }

class CommentForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class":"form-control"}))

    class Meta:
        model = Comment
        fields = ["name","email","body"]
        widgets = {"body": forms.Textarea(attrs={"class":"form-control","rows":4})}
