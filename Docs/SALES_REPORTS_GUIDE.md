# Sales Reports App Documentation

## Revenue Calculation Policy

**Important**: Revenue is calculated ONLY from orders with status "delivered". This ensures accurate financial reporting by counting only completed transactions where payment has been received and products have been successfully delivered to customers.

### Revenue Rules:
- ✅ **Delivered orders**: Count towards revenue
- ❌ **Pending orders**: Do not count towards revenue
- ❌ **Confirmed orders**: Do not count towards revenue  
- ❌ **Processing orders**: Do not count towards revenue
- ❌ **Shipped orders**: Do not count towards revenue
- ❌ **Cancelled orders**: Do not count towards revenue
- ❌ **Refunded orders**: Do not count towards revenue

This conservative approach ensures that revenue figures represent actual completed business transactions.
The Reports app provides comprehensive sales analytics and reporting functionality for the e-commerce platform. It is specifically designed for business owners to track sales performance, monitor customer behavior, and analyze product trends.

## Features

### 1. Dashboard
- **URL**: `/reports/`
- **Access**: Owner role only
- **Features**:
  - Quick stats for the last 30 days
  - Recent orders overview
  - Top-selling products
  - Revenue and order metrics

### 2. Sales Reports
- **URL**: `/reports/sales/`
- **Features**:
  - Customizable date range filtering
  - Order status breakdown
  - Daily sales trends
  - Export functionality (CSV, JSON)
  - Performance metrics

### 3. Product Reports
- **URL**: `/reports/products/`
- **Features**:
  - Product performance ranking
  - Units sold and revenue by product
  - Performance indicators (Excellent, Good, Average, Poor)
  - Top performers and underperforming products identification

### 4. Customer Reports
- **URL**: `/reports/customers/`
- **Features**:
  - Customer ranking by spending
  - Customer tier classification (VIP, Premium, Regular, New)
  - Loyalty indicators
  - Customer lifetime value analysis

## Models

### SalesReport
- Stores generated sales reports for caching and history
- Fields: report_type, start_date, end_date, metrics, generated_by

### ProductSalesReport
- Tracks product-specific sales data
- Links to SalesReport and Product models

### CustomerSalesReport
- Tracks customer-specific sales data
- Links to SalesReport and User models

## Access Control
- **Owner Role Required**: All reports functionality is restricted to users with 'owner' role
- **Decorator**: `@owner_required` is used on all views
- **Navigation**: Reports link appears in Management dropdown only for owners

## Installation Steps

1. Add 'reports' to INSTALLED_APPS in settings.py
2. Run migrations: `python manage.py makemigrations reports && python manage.py migrate`
3. Add reports URLs to main urls.py
4. Ensure owner users exist in the system

## Usage

### Creating an Owner User
```python
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create user
user = User.objects.create_user(
    username='owner',
    email='owner@example.com',
    password='password',
    first_name='Business',
    last_name='Owner'
)

# Set as owner
profile = user.profile
profile.role = 'owner'
profile.save()
```

### Generating Sample Report
```bash
python manage.py generate_sample_report --days=30 --report-type=monthly
```

## Navigation Integration
The reports functionality is integrated into the main navigation:
- Management dropdown → Sales Reports (for owners only)
- Located in the Management section alongside other admin tools

## Export Functionality
Reports can be exported in multiple formats:
- **CSV**: Tabular data for spreadsheet analysis
- **JSON**: Structured data for API consumption
- **PDF**: Formatted reports for presentation (future enhancement)

## Performance Considerations
- Reports are generated on-demand for accuracy
- Consider implementing caching for frequently accessed reports
- Database queries are optimized with proper indexing
- Large date ranges may require pagination

## Future Enhancements
- PDF export functionality
- Automated report scheduling
- Email report delivery
- Advanced analytics with charts and graphs
- Inventory reports
- Profit margin analysis

## Security
- All views protected with login_required and owner_required decorators
- CSRF protection for export functionality
- Data filtering ensures users only see authorized data

## Testing
Use the management command to generate sample reports:
```bash
python manage.py generate_sample_report
```

This will create a test report using existing order data in the system.
