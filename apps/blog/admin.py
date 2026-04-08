from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # prepopulated_fields = when you type the name in admin
    # Django automatically fills the slug field!
    # "Django Tips" → "django-tips" — auto filled


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display   = ('title', 'author', 'category', 'status', 'created_at')
    list_filter    = ('status', 'category', 'created_at')
    search_fields  = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields  = ('author',)
    # raw_id_fields = for author field, show ID input instead of
    # loading ALL users in a dropdown — better for performance
    ordering       = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('author', 'post', 'created_at')
    search_fields = ('content', 'author__full_name')
    # author__full_name = Django double underscore
    # searches across related model fields