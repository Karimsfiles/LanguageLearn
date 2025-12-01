from django.contrib import admin
from .models import Language, Word, FavoriteWord

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('original_word', 'translation', 'language_from', 'language_to', 'added_by', 'date_added')
    list_filter = ('language_from', 'language_to', 'date_added', 'added_by')
    search_fields = ('original_word', 'translation')
    fieldsets = (
        (None, {
            'fields': ('original_word', 'translation')
        }),
        ('Языки', {
            'fields': ('language_from', 'language_to')
        }),
        ('Дополнительно', {
            'fields': ('example_sentence', 'added_by'),
            'classes': ('collapse',)
        })
    )

@admin.register(FavoriteWord)
class FavoriteWordAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'date_added')
    list_filter = ('user', 'date_added')
    search_fields = ('user__username', 'word__original_word', 'word__translation')