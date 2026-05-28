from django.shortcuts import render

# Create your views here.
# tracker/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Product, PriceHistory
from .serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    PriceHistorySerializer,
)


class ProductListCreateView(APIView):
    """
    GET  /api/products/  → list all active products
    POST /api/products/  → add a new product to track
    """

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save()
            # Return full product data after creation, not just the URL
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductPriceHistoryView(APIView):
    """
    GET /api/products/<id>/history/ → price history for a specific product
    """

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, is_active=True)
        history = product.price_history.all()  # uses related_name we set in Phase 2

        return Response({
            'product': ProductSerializer(product).data,
            'history': PriceHistorySerializer(history, many=True).data,
        })