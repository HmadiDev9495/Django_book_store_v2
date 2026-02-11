from django.contrib import admin
from .models import Book, ImageBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'price_with_currency', 'published_date', 'get_image_count')
    list_filter = ('category', 'currency')
    search_fields = ('name', 'author')

    def get_image_count(self, obj):
        return obj.images.count()

    get_image_count.short_description = 'تعداد تصاویر'

admin.site.register(ImageBook)