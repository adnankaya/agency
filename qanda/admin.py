from django.contrib import admin

from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'is_active')
    list_filter = ('is_active', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    # removes combobox, creates search text input field
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('publish',)