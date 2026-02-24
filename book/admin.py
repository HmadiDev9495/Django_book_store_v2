from django.contrib import admin
from .models import Book, ImageBook, APILearningLog


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'price_with_currency', 'published_date', 'get_image_count')
    list_filter = ('category', 'currency')
    search_fields = ('name', 'author')

    def get_image_count(self, obj):
        return obj.images.count()

    get_image_count.short_description = 'تعداد تصاویر'

admin.site.register(ImageBook)


@admin.register(APILearningLog)
class APILearningLogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'method', 'url_short', 'user',
        'response_time_ms', 'is_slow_colored',
        'status_code', 'created_at'
    )
    list_filter = ('is_slow', 'method', 'status_code', 'created_at')
    search_fields = ('url', 'user__username', 'ip_address')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def url_short(self, obj):
        """نمایش کوتاه URL"""
        url = obj.url
        return url[:50] + '...' if len(url) > 50 else url

    url_short.short_description = 'آدرس'

    def is_slow_colored(self, obj):

        if obj.is_slow:
            return "🐌 کند"
        return "⚡ سریع"

    is_slow_colored.short_description = 'وضعیت سرعت'