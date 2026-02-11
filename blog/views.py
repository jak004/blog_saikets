from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from .forms import PostForm, CommentForm

def home(request):
    featured = Post.objects.filter(status="published", featured=True).order_by("-published_at")[:3]
    latest = Post.objects.filter(status="published").order_by("-published_at")[:10]
    return render(request, "blog/home.html", {"featured": featured, "latest": latest})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    comments = post.comments.filter(is_approved=True, is_hidden=False).order_by("-created_at")

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post

            if request.user.is_authenticated:
                c.user = request.user
                c.name = ""
                c.email = ""
            else:
                name = (form.cleaned_data.get("name") or "").strip()
                email = (form.cleaned_data.get("email") or "").strip()
                if not name or not email:
                    messages.error(request, "Guest comments require your name and email.")
                    return redirect("post_detail", slug=slug)
                c.name = name
                c.email = email

            c.is_approved = False
            c.save()
            messages.success(request, "Comment submitted for moderation.")
            return redirect("post_detail", slug=slug)

    return render(request, "blog/post_detail.html", {"post": post, "comments": comments, "form": form})

def list_posts(request):
    q = (request.GET.get("q") or "").strip()
    cat = (request.GET.get("category") or "").strip()
    tag = (request.GET.get("tag") or "").strip()

    posts = Post.objects.filter(status="published").order_by("-published_at")

    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))
    if cat:
        posts = posts.filter(category__slug=cat)
    if tag:
        posts = posts.filter(tags__slug=tag)

    categories = Category.objects.all().order_by("name")
    tags = Tag.objects.all().order_by("name")

    return render(request, "blog/list.html", {
        "posts": posts, "q": q, "categories": categories, "tags": tags, "cat": cat, "tag": tag
    })

def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status="published", category=category).order_by("-published_at")
    return render(request, "blog/list_simple.html", {"title": f"Category: {category.name}", "posts": posts})

def posts_by_tag(request, slug):
    tag_obj = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status="published", tags=tag_obj).order_by("-published_at")
    return render(request, "blog/list_simple.html", {"title": f"Tag: {tag_obj.name}", "posts": posts})

@login_required
def dashboard(request):
    my_posts = Post.objects.filter(author=request.user).order_by("-updated_at")
    return render(request, "blog/dashboard.html", {"posts": my_posts})

@login_required
def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post saved.")
            return redirect("dashboard")
    return render(request, "blog/post_form.html", {"form": form, "title": "Create Post"})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            form.save_m2m()
            messages.success(request, "Post updated.")
            return redirect("dashboard")
    return render(request, "blog/post_form.html", {"form": form, "title": "Edit Post"})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("dashboard")
    return render(request, "blog/post_delete.html", {"post": post})
