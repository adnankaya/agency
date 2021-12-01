from django.contrib import admin

from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'published_date', 'is_active')
    list_filter = ('is_active', 'created_date', 'published_date', 'author')
    search_fields = ('text', )
    # removes combobox, creates search text input field
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('published_date',)