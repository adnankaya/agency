from django.contrib import admin

# Register your models here.
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    # removes combobox, creates search text input field
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('made_by', 'email', 'post', 'created', 'is_active')
    list_filter = ('is_active', 'created', 'updated')
    search_fields = ('made_by', 'email', 'body')
    
