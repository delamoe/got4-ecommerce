from .models import Product, Category
from django.test import TestCase
from django.urls import reverse

class ProductModelTests(TestCase):
    
    def setUp(self):
        # Create a category for use in product creation
        self.category = Category.objects.create(name="Electronics", description="Gadgets and gizmos.")
        
        # Create a product
        self.product = Product.objects.create(
            name="Test Product",
            description="A test product description.",
            price=9.99,
            inventory_count=100,
            available=True,
            category=self.category
        )

    def test_product_creation(self):
        """Test that a product is correctly created with its fields."""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "A test product description.")
        self.assertEqual(self.product.price, 9.99)
        self.assertEqual(self.product.inventory_count, 100)
        self.assertEqual(self.product.available, True)
        self.assertEqual(self.product.category.name, "Electronics")

    def test_product_str(self):
        """Test the product string representation."""
        self.assertEqual(str(self.product), "Test Product")


class ProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_products = 10
        for product_id in range(number_of_products):
            Product.objects.create(
                name=f'Product {product_id}',
                description='Test Description',
                price=9.99,
                inventory_count=100,
                available=True,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('product_list'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['product_list']) == 5)

    def test_lists_all_products(self):
        # Create more products to test pagination
        number_of_products = 13
        for product_id in range(5, number_of_products):
            Product.objects.create(
                name=f'Product {product_id}',
                description='Test Description',
                price=9.99,
                inventory_count=100,
                available=True,
            )
        response = self.client.get(reverse('product_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['product_list']) == 5)


class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name='Test Product Detail',
            description='Detail Description',
            price=19.99,
            inventory_count=50,
            available=True,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_view_shows_product_content(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('product' in response.context)
        # Check that the product details are correct
        self.assertEqual(response.context['product'].name, 'Test Product Detail')
        self.assertEqual(response.context['product'].description, 'Detail Description')
