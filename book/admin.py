from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'price_with_currency', 'published_date')
    list_filter = ('category', 'currency')
    search_fields = ('name', 'author')