from django.db import models

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

    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100, blank=True)
    published_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default='FN')
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='TOMAN')
    page_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def price_with_currency(self):
        if self.currency == 'TOMAN':
            return f"{self.price:,.0f} Toman"
        else:
            return f"${self.price:,.2f}"

    price_with_currency.short_description = 'Price'

    def __str__(self):
        return self.name