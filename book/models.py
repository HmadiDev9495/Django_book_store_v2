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
    publisher_name = models.CharField(max_length=100, blank=True)  # نام ناشر (متنی)
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