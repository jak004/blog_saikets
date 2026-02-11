from django.contrib import admin
from .models import Post, Category, Tag, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","status","featured","published_at","updated_at")
    list_filter = ("status","featured","category","tags")
    search_fields = ("title","excerpt","content")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post","display_name","is_approved","is_hidden","created_at")
    list_filter = ("is_approved","is_hidden")
    search_fields = ("body","name","email","user__username","post__title")
    actions = ["approve_comments","hide_comments","unhide_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    def hide_comments(self, request, queryset):
        queryset.update(is_hidden=True)

    def unhide_comments(self, request, queryset):
        queryset.update(is_hidden=False)

admin.site.register(Category)
admin.site.register(Tag)
