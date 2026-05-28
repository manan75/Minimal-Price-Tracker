from django.db import models

# Create your models here.
# tracker/models.py


class Product(models.Model):

    class SiteChoices(models.TextChoices):
        AMAZON = 'amazon', 'Amazon'
        FLIPKART = 'flipkart', 'Flipkart'
        UNKNOWN = 'unknown', 'Unknown'

    url = models.URLField(unique=True)
    name = models.CharField(max_length=500, blank=True)  # filled after first scrape
    site = models.CharField(
        max_length=50,
        choices=SiteChoices.choices,
        default=SiteChoices.UNKNOWN,
    )
    is_active = models.BooleanField(default=True)  # pause tracking without deleting
    created_at = models.DateTimeField(auto_now_add=True)
    last_checked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name or self.url

    def latest_price(self):
        entry = self.price_history.first()  # ordered by -scraped_at already
        return entry.price if entry else None


class PriceHistory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='price_history',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scraped_at']

    def __str__(self):
        return f"{self.product.name} → ₹{self.price} at {self.scraped_at:%Y-%m-%d %H:%M}"