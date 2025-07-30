# Role-Based Access Control System

## Overview

I have successfully implemented a comprehensive role-based access control system for your Django e-commerce application. The system provides three distinct user roles with different levels of access and permissions.

## 🎭 User Roles

### 1. **Customer** 👤
- **Default role** for new registered users
- **Access Level**: Basic browsing capabilities
- **Permissions**:
  - ✅ Browse home page
  - ✅ View product list
  - ✅ View individual product details
  - ✅ Manage their own profile
  - ❌ Cannot add/edit/delete products
  - ❌ Cannot access dashboard
  - ❌ Cannot access admin panel

### 2. **Staff** 👷
- **Role for employees** who manage products
- **Access Level**: Product management capabilities
- **Permissions**:
  - ✅ All customer permissions
  - ✅ Add new products
  - ✅ Edit existing products
  - ✅ Delete products
  - ✅ Access dashboard
  - ❌ Cannot access admin panel
  - ❌ Cannot change user roles

### 3. **Owner/Admin** 👑
- **Highest privilege level** for site owners
- **Access Level**: Full system control
- **Permissions**:
  - ✅ All staff permissions
  - ✅ Access Django admin panel
  - ✅ Manage user roles
  - ✅ Full administrative control
  - ✅ Superuser privileges

### 4. **Anonymous Users** 🌐
- **Unregistered visitors**
- **Access Level**: Public browsing only
- **Permissions**:
  - ✅ Browse home page
  - ✅ View product list
  - ✅ View individual product details
  - ❌ Cannot see edit/delete buttons
  - ❌ Cannot access any management features

## 🔧 Technical Implementation

### **Automatic Role Assignment**
- **New Users**: Automatically assigned `customer` role
- **Staff Users**: `is_staff=True` → automatically assigned `staff` role
- **Superusers**: `is_superuser=True` → automatically assigned `owner` role

### **Signal-Based Profile Creation**
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'customer'  # Default
        if instance.is_superuser:
            role = 'owner'
        elif instance.is_staff:
            role = 'staff'
        UserProfile.objects.create(user=instance, role=role)
```

### **Role-Based Decorators**
```python
@staff_or_owner_required
def add_product(request):
    # Only staff and owners can access
    
@owner_required
def admin_function(request):
    # Only owners can access
```

## 🎯 Access Control Matrix

| Feature | Anonymous | Customer | Staff | Owner |
|---------|-----------|----------|-------|-------|
| Browse Home Page | ✅ | ✅ | ✅ | ✅ |
| View Products | ✅ | ✅ | ✅ | ✅ |
| Product Details | ✅ | ✅ | ✅ | ✅ |
| User Registration | ✅ | ❌ | ❌ | ❌ |
| User Login | ✅ | ✅ | ✅ | ✅ |
| Profile Management | ❌ | ✅ | ✅ | ✅ |
| Add Products | ❌ | ❌ | ✅ | ✅ |
| Edit Products | ❌ | ❌ | ✅ | ✅ |
| Delete Products | ❌ | ❌ | ✅ | ✅ |
| Dashboard Access | ❌ | ❌ | ✅ | ✅ |
| Admin Panel | ❌ | ❌ | ❌ | ✅ |
| Role Management | ❌ | ❌ | ❌ | ✅ |

## 🎨 UI/UX Features

### **Dynamic Navigation**
- Navigation menu adapts based on user role
- Action buttons show/hide based on permissions
- Role display in user info section

### **Role-Based Redirects**
- **Customer login** → Home page
- **Staff/Owner login** → Dashboard
- **Logout** → Home page

### **Conditional Template Elements**
```django
{% if user.is_authenticated and user.profile.can_manage_products %}
    <a href="{% url 'products:add_product' %}">Add Product</a>
{% endif %}
```

## 🚀 Test Users Created

The system includes pre-created test users for each role:

| Username | Password | Role | Purpose |
|----------|----------|------|---------|
| `customer_user` | `customer123` | Customer | Test customer experience |
| `staff_user` | `staff123` | Staff | Test product management |
| `owner_user` | `owner123` | Owner/Admin | Test full admin access |

## 🔐 Security Features

### **Access Control Decorators**
- `@login_required` - Requires authentication
- `@staff_or_owner_required` - Requires staff or owner role
- `@owner_required` - Requires owner role only

### **Permission Checking Methods**
```python
user.profile.can_access_admin()      # Owner only
user.profile.can_manage_products()   # Staff + Owner
user.profile.can_access_dashboard()  # Staff + Owner
```

### **Automatic Role Synchronization**
- User roles automatically sync with Django's `is_staff` and `is_superuser`
- Role changes trigger profile updates via signals

## 📁 Files Modified/Created

### **Enhanced Models**
- `accounts/models.py` - Added role field and permission methods
- Role choices: customer, staff, owner
- Automatic role assignment via signals

### **Access Control System**
- `accounts/decorators.py` - Role-based view decorators
- Permission checking functions
- Flexible role validation

### **Enhanced Views**
- Role-based redirects after login
- Protected product management views
- Protected dashboard access

### **Enhanced Templates**
- Dynamic navigation based on roles
- Conditional action buttons
- Role display in user info

### **Admin Integration**
- Enhanced user admin with role filtering
- Inline profile editing
- Role-based user management

## 🎮 How to Test the System

### **1. Test Anonymous Access**
```bash
# Visit without logging in
http://127.0.0.1:8000/
```
- ✅ Can browse home and products
- ❌ No edit/delete buttons visible
- ❌ Cannot access dashboard or admin

### **2. Test Customer Role**
```bash
# Login as customer
Username: customer_user
Password: customer123
```
- ✅ Can view all public content
- ✅ Can manage own profile
- ❌ Cannot see product management options
- ❌ Dashboard link not visible

### **3. Test Staff Role**
```bash
# Login as staff
Username: staff_user
Password: staff123
```
- ✅ Can manage products (add/edit/delete)
- ✅ Can access dashboard
- ✅ Product management buttons visible
- ❌ Cannot access admin panel

### **4. Test Owner Role**
```bash
# Login as owner
Username: owner_user
Password: owner123
```
- ✅ Full access to all features
- ✅ Admin panel link visible
- ✅ Can change user roles
- ✅ Complete system control

## 🔄 Role Management

### **Changing User Roles**

**Option 1: Django Admin**
1. Login as owner/superuser
2. Go to Admin Panel → Users
3. Edit user → Profile section → Change role

**Option 2: Profile Edit (Owner Only)**
1. Login as owner
2. Edit any user's profile
3. Role dropdown appears for owners

### **Automatic Role Updates**
- Making user `is_staff=True` → Upgrades to staff role
- Making user `is_superuser=True` → Upgrades to owner role
- Removing staff status → May downgrade to customer

## 🧪 Testing Commands

```bash
# Run all role-based tests
python manage.py test accounts

# Create/reset test users
python manage.py create_test_users --reset

# Check user roles in shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.get(username='staff_user').profile.role
```

## 🎉 Benefits Achieved

1. **Security**: Proper access control prevents unauthorized actions
2. **Flexibility**: Easy to add new roles or modify permissions
3. **User Experience**: Clear role-based navigation and features
4. **Scalability**: System can grow with more complex role requirements
5. **Testing**: Comprehensive test coverage ensures reliability
6. **Admin Friendly**: Easy role management through Django admin

The role-based access control system is now fully functional and provides a secure, scalable foundation for managing different user types in your e-commerce application!
