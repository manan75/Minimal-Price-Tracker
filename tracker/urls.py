# tracker/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/history/', views.ProductPriceHistoryView.as_view(), name='product-history'),
]