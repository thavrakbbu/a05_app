# E-commerce Project Structure

This Django project has been refactored to separate concerns between the `store` and `products` apps.

## App Structure

### Store App (`store/`)
**Purpose**: Handles the main store functionality, frontend views, and shopping experience.

**Responsibilities**:
- Home page displaying products
- Store dashboard with statistics
- Shopping cart (future feature)
- Order management (future feature)
- Customer management (future feature)

**Key Files**:
- `views.py`: Home page and dashboard views
- `urls.py`: Store-related URL patterns
- `templates/`: Store-specific templates (home, dashboard, base)

### Products App (`products/`)
**Purpose**: Handles all product-related functionality and management.

**Responsibilities**:
- Product model and category model
- Product CRUD operations (Create, Read, Update, Delete)
- Product catalog management
- Category management
- Product admin interface

**Key Files**:
- `models.py`: Product and Category models
- `views.py`: Product management views (list, add, edit, delete, detail)
- `forms.py`: Product forms
- `admin.py`: Product admin configuration
- `urls.py`: Product-related URL patterns
- `templates/products/`: Product-specific templates

## URL Structure

- `/` - Home page (store app)
- `/dashboard/` - Store dashboard (store app)
- `/products/` - Product list (products app)
- `/products/add/` - Add new product (products app)
- `/products/<id>/` - Product detail (products app)
- `/products/<id>/edit/` - Edit product (products app)
- `/products/<id>/delete/` - Delete product (products app)

## Navigation

The navigation has been updated to reflect the new structure:
- **Home**: Store front page
- **Products**: Product management list
- **Add Product**: Quick access to add products
- **Dashboard**: Store overview and statistics

## Database Migration

The project has been migrated from having Product and Category models in the store app to having them in the products app. The data has been preserved during this migration.

## Benefits of This Structure

1. **Separation of Concerns**: Each app has a clear, focused responsibility
2. **Scalability**: Easy to add new features to either store or product management
3. **Maintainability**: Changes to product functionality don't affect store functionality
4. **Reusability**: The products app can be reused in other projects
5. **Team Development**: Different developers can work on different apps simultaneously

## Future Enhancements

With this structure, you can easily add:
- Shopping cart functionality (store app)
- Order management (new orders app)
- Customer management (new customers app)
- Inventory management (products app)
- Product reviews (products app)
- Payment processing (new payments app)
