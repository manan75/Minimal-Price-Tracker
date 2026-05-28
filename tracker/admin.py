from django.contrib import admin

# Register your models here.
# tracker/admin.py

from .models import Product, PriceHistory


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0
    readonly_fields = ('price', 'scraped_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'is_active', 'latest_price', 'last_checked_at', 'created_at')
    list_filter = ('site', 'is_active')
    search_fields = ('name', 'url')
    inlines = [PriceHistoryInline]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'scraped_at')
    list_filter = ('product',)