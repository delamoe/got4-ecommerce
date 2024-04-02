# products/tests.py
from django.test import TestCase
from .models import Product


class ProductTestCase(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name="Test Product", price=10.99)
        self.assertEqual(product.name, "Test Product")


class ProductTests(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name="Test Product", price=100)
        self.assertEqual(product.name, "Test Product")
