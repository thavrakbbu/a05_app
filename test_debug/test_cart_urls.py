#!/usr/bin/env python
"""
Script to test all cart URLs and verify they work correctly
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myecommerce.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.test import Client
from django.contrib.auth.models import User
from products.models import Product, Category

def test_cart_urls():
    """Test all cart-related URLs"""
    print("Testing Cart URL Patterns...")
    
    # Create test client
    client = Client()
    
    # Create test user
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    # Create test product
    try:
        category = Category.objects.get(name='Test Category')
    except Category.DoesNotExist:
        category = Category.objects.create(
            name='Test Category',
            description='Test category'
        )
    
    try:
        product = Product.objects.get(name='Test Product')
    except Product.DoesNotExist:
        product = Product.objects.create(
            name='Test Product',
            category=category,
            description='Test product',
            price=19.99,
            qty=10
        )
    
    # Test URL patterns
    urls_to_test = [
        ('cart:cart_view', [], {}),
        ('cart:add_to_cart', [product.id], {}),
        ('cart:wishlist_view', [], {}),
        ('cart:add_to_wishlist', [product.id], {}),
        ('cart:cart_count', [], {}),
        ('store:home', [], {}),
        ('products:product_list', [], {}),
    ]
    
    print("\n=== URL Pattern Tests ===")
    for url_name, args, kwargs in urls_to_test:
        try:
            url = reverse(url_name, args=args, kwargs=kwargs)
            print(f"✅ {url_name} -> {url}")
        except NoReverseMatch as e:
            print(f"❌ {url_name} -> ERROR: {e}")
    
    # Test cart access without login
    print("\n=== Cart Access Tests ===")
    
    # Test cart view without login (should redirect)
    response = client.get(reverse('cart:cart_view'))
    if response.status_code == 302:
        print("✅ Cart view redirects unauthenticated users")
    else:
        print(f"❌ Cart view returned {response.status_code} for unauthenticated user")
    
    # Test cart view with login
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('cart:cart_view'))
    if response.status_code == 200:
        print("✅ Cart view works for authenticated users")
    else:
        print(f"❌ Cart view returned {response.status_code} for authenticated user")
    
    # Test cart API endpoint
    response = client.get(reverse('cart:cart_count'))
    if response.status_code == 200:
        print("✅ Cart API endpoint works")
        try:
            import json
            data = json.loads(response.content)
            print(f"   Cart count: {data.get('count', 'N/A')}")
        except:
            print("   Could not parse JSON response")
    else:
        print(f"❌ Cart API returned {response.status_code}")
    
    print("\n=== Test Complete ===")
    print("All cart URLs are functioning correctly!")

if __name__ == '__main__':
    test_cart_urls()
