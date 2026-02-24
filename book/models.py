from django.db import models
from django.conf import settings


class Book(models.Model):
    CATEGORY_CHOICES = [
        ('SC', 'Science'),
        ('FN', 'Fun'),
        ('HC', 'Historical'),
        ('RM', 'Romance'),
        ('TH', 'Thriller'),
    ]

    CURRENCY_CHOICES = [
        ('TOMAN', 'Toman'),
        ('USD', 'US Dollar'),
    ]


    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='ناشر',
        null=True,
        blank=True
    )


    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    published_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='FN')
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='TOMAN')
    page_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    publisher_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def price_with_currency(self):
        if self.price is None:
            return "قیمت نامشخص"
        if self.currency == 'TOMAN':
            return f"{self.price:,.0f} Toman"
        else:
            return f"${self.price:,.2f}"

    price_with_currency.short_description = 'Price'

    def __str__(self):
        return self.name



class BaseBook(models.Model):
    name = models.CharField(max_length=50)
    published_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class DifferentBook(BaseBook):
    pass


class ImageBook(models.Model):
    name = models.CharField(max_length=50, verbose_name="Image Name")

    image = models.ImageField(upload_to='book_images/', verbose_name='تصویر', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images",
                             related_query_name="image_query")

    class Meta:
        verbose_name = "Images of Book"

    def __str__(self):
        return self.name


class APILearningLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='api_logs',
        verbose_name='کاربر'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='آدرس IP'
    )
    method = models.CharField(
        max_length=10,
        verbose_name='متد HTTP'
    )
    url = models.URLField(
        verbose_name='آدرس'
    )
    status_code = models.PositiveIntegerField(
        verbose_name='کد وضعیت'
    )
    response_time_ms = models.FloatField(
        verbose_name='زمان پاسخ (میلی‌ثانیه)'
    )
    is_slow = models.BooleanField(
        default=False,
        verbose_name='آیا کند بود؟'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='مرورگر'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان'
    )

    class Meta:
        verbose_name = 'لاگ آموزشی API'
        verbose_name_plural = 'لاگ‌های آموزشی API'
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['is_slow']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        speed = "🐌" if self.is_slow else "⚡"
        return f"{speed} [{self.id}] {self.method} {self.url} ({self.response_time_ms:.0f}ms) - {user_str}"

    @property
    def is_success(self):

        return 200 <= self.status_code < 300

    @property
    def time_category(self):

        if self.response_time_ms < 100:
            return "سریع 🚀"
        elif self.response_time_ms < 500:
            return "متوسط ⏱️"
        else:
            return "کند 🐢"