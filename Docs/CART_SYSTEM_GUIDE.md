# Cart Management System Documentation

## Overview
The cart management system is a Django app that provides shopping cart and wishlist functionality for customers in the e-commerce application.

## Features

### 🛒 Shopping Cart
- **Add to Cart**: Add products with specified quantities
- **Update Quantities**: Modify item quantities in cart
- **Remove Items**: Remove individual items or clear entire cart
- **Stock Validation**: Prevents adding more items than available stock
- **Price Calculation**: Automatic total price calculation
- **Persistent Storage**: Cart data is saved to database

### ❤️ Wishlist
- **Save for Later**: Add products to wishlist
- **Move to Cart**: Transfer items from wishlist to cart
- **Remove Items**: Remove items from wishlist
- **Quick Access**: Easy access to saved products

### 🔧 Additional Features
- **AJAX Support**: Real-time cart count updates
- **Context Processor**: Cart information available globally
- **Responsive Design**: Mobile-friendly interface
- **User Authentication**: Requires login for cart/wishlist access

## Models

### Cart Model
```python
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### CartItem Model
```python
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
```

### WishList Model
```python
class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## URL Patterns

### Cart URLs
- `/cart/` - View shopping cart
- `/cart/add/<int:product_id>/` - Add product to cart
- `/cart/update/<int:item_id>/` - Update cart item quantity
- `/cart/remove/<int:item_id>/` - Remove item from cart
- `/cart/clear/` - Clear entire cart

### Wishlist URLs
- `/cart/wishlist/` - View wishlist
- `/cart/wishlist/add/<int:product_id>/` - Add to wishlist
- `/cart/wishlist/remove/<int:product_id>/` - Remove from wishlist
- `/cart/wishlist/move-to-cart/<int:product_id>/` - Move to cart

### AJAX URLs
- `/cart/api/count/` - Get cart item count
- `/cart/api/quick-add/` - Quick add to cart

## Views

### Key View Functions
1. **cart_view**: Display shopping cart with all items
2. **add_to_cart**: Add products to cart with quantity validation
3. **update_cart_item**: Update item quantities
4. **wishlist_view**: Display wishlist items
5. **cart_count**: AJAX endpoint for cart count

## Templates

### Cart Templates
- `cart/cart.html` - Main shopping cart page
- `cart/wishlist.html` - Wishlist page

### Template Features
- Responsive design with Bootstrap-like styling
- Real-time quantity updates
- Stock validation feedback
- Empty state handling

## Admin Interface

### Cart Admin Features
- View all user carts
- Inline cart item editing
- Total price calculations
- Search and filtering

### Admin Models
- CartAdmin: Manage user carts
- CartItemAdmin: Manage individual cart items
- WishListAdmin: Manage user wishlists

## Security Features

### Authentication
- All cart operations require user login
- User can only access their own cart/wishlist
- CSRF protection on all forms

### Data Validation
- Stock quantity validation
- Positive integer quantities only
- Product existence validation

## Usage Examples

### Adding to Cart from Product Page
```html
<form method="post" action="{% url 'cart:add_to_cart' product.id %}">
    {% csrf_token %}
    <input type="number" name="quantity" value="1" min="1" max="{{ product.qty }}">
    <button type="submit">Add to Cart</button>
</form>
```

### Quick Add via AJAX
```javascript
fetch('{% url "cart:quick_add_to_cart" %}', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        'product_id': productId,
        'quantity': 1
    })
})
```

## Integration with Existing Apps

### Products App Integration
- Cart buttons added to product list and detail pages
- Stock validation against product quantities
- Price calculation using product prices

### Accounts App Integration
- User authentication required
- User profile integration for permissions
- Cart/wishlist tied to user accounts

### Navigation Integration
- Cart link in main navigation
- Real-time cart count display
- Cart and wishlist icons with Font Awesome

## Testing

### Test Coverage
- Cart creation and management
- Product addition/removal
- Stock validation
- Wishlist functionality
- AJAX endpoints

### Running Tests
```bash
python manage.py test cart
```

## Configuration

### Settings Required
```python
INSTALLED_APPS = [
    # ... other apps
    'cart',
]

TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... other processors
                'cart.context_processors.cart_processor',
            ],
        },
    },
]
```

### Dependencies
- Django 5.2+
- Font Awesome (for icons)
- Bootstrap-compatible CSS

## Future Enhancements

### Potential Features
- 🚀 Checkout and payment integration
- 📧 Abandoned cart email notifications
- 🎯 Product recommendations
- 📊 Cart analytics
- 💾 Guest cart functionality
- 🏷️ Coupon and discount codes
- 📱 Mobile app API endpoints

### Performance Optimizations
- Cart caching with Redis
- Bulk operations for cart updates
- Database query optimization
- CDN integration for static files

## Troubleshooting

### Common Issues
1. **Cart count not updating**: Check AJAX endpoint and CSRF token
2. **Permission denied**: Ensure user is authenticated
3. **Stock errors**: Verify product quantities are up to date
4. **Template not found**: Check template paths and app registration

### Debug Tips
- Enable Django debug mode for detailed error messages
- Check browser console for JavaScript errors
- Verify URL patterns are correctly configured
- Test with different user roles and permissions

## Support
For questions or issues with the cart system, please check:
1. Django logs for backend errors
2. Browser console for frontend errors
3. Database for data consistency
4. Test suite for regression testing
