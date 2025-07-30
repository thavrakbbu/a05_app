from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db import transaction
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import json
import uuid

from .models import Order, OrderItem, ShippingMethod, Coupon, OrderCoupon
from payment.models import Payment
from cart.models import Cart, CartItem
from products.models import Product


@login_required
def order_list(request):
    """Display user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Count orders by status
    pending_count = orders.filter(status='pending').count()
    confirmed_count = orders.filter(status='confirmed').count()
    processing_count = orders.filter(status='processing').count()
    shipped_count = orders.filter(status='shipped').count()
    delivered_count = orders.filter(status='delivered').count()
    cancelled_count = orders.filter(status='cancelled').count()
    
    context = {
        'orders': orders,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'processing_count': processing_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
        'cancelled_count': cancelled_count,
        'total_count': orders.count(),
    }
    
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
@require_POST
def mark_order_delivered(request, order_id):
    """Mark order as delivered by customer"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if order.status != 'shipped':
        messages.error(request, 'Order must be shipped before marking as delivered.')
        return redirect('orders:order_detail', order_id=order_id)
    
    order.status = 'delivered'
    order.save()
    
    messages.success(request, 'Order marked as delivered successfully!')
    return redirect('orders:order_detail', order_id=order_id)


# Admin views (moved from payment app)
@login_required
def admin_order_list(request):
    """Admin view for listing all orders"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff privileges required.')
        return redirect('store:home')
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    # Base queryset with optimized queries
    orders = Order.objects.select_related('user').prefetch_related(
        'order_items__product',
        'payment'
    )
    
    # Calculate statistics for all orders (before filtering)
    from django.db.models import Count
    all_orders_stats = Order.objects.values('status').annotate(count=Count('id'))
    status_dict = {item['status']: item['count'] for item in all_orders_stats}
    
    total_orders = Order.objects.count()
    pending_orders = status_dict.get('pending', 0)
    confirmed_orders = status_dict.get('confirmed', 0)
    processing_orders = status_dict.get('processing', 0)
    shipped_orders = status_dict.get('shipped', 0)
    delivered_orders = status_dict.get('delivered', 0)
    cancelled_orders = status_dict.get('cancelled', 0)
    refunded_orders = status_dict.get('refunded', 0)
    
    # Apply filters to the display queryset
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if search_query:
        orders = orders.filter(
            models.Q(order_id__icontains=search_query) |
            models.Q(user__username__icontains=search_query) |
            models.Q(user__email__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query)
        )
    
    # Order by creation date (newest first)
    orders = orders.order_by('-created_at')
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
        'order_status_choices': Order.ORDER_STATUS_CHOICES,
        # Add statistics
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'refunded_orders': refunded_orders,
    }
    
    return render(request, 'orders/admin/order_list.html', context)


@login_required
def admin_order_detail(request, order_id):
    """Admin view for order details"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff privileges required.')
        return redirect('store:home')
    
    order = get_object_or_404(
        Order.objects.select_related('user').prefetch_related(
            'order_items__product',
            'payment'
        ),
        order_id=order_id
    )
    
    context = {
        'order': order,
        'order_status_choices': Order.ORDER_STATUS_CHOICES,
    }
    
    return render(request, 'orders/admin/order_detail.html', context)


@login_required
@require_POST
def update_order_status(request, order_id):
    """Update order status via AJAX"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    order = get_object_or_404(Order, order_id=order_id)
    new_status = request.POST.get('status')
    
    if new_status not in dict(Order.ORDER_STATUS_CHOICES):
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    
    old_status = order.status
    order.status = new_status
    order.save()
    
    # Update payment status when order status changes
    if hasattr(order, 'payment') and order.payment:
        payment = order.payment
        
        # Update payment status based on order status
        if new_status == 'confirmed' and payment.status == 'pending':
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()
        elif new_status == 'cancelled' and payment.status in ['pending', 'processing']:
            payment.status = 'cancelled'
            payment.save()
        elif new_status in ['processing', 'shipped'] and payment.status == 'pending':
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()
        elif new_status == 'delivered' and payment.status != 'completed':
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()
    
    return JsonResponse({
        'success': True,
        'new_status': new_status,
        'new_status_display': order.get_status_display(),
        'payment_status': order.payment.status if hasattr(order, 'payment') and order.payment else None
    })


@login_required
def admin_dashboard(request):
    """Admin dashboard with order statistics"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff privileges required.')
        return redirect('store:home')
    
    # Get order statistics using aggregation for better performance
    from django.db.models import Count
    
    # Get counts for each status
    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    status_dict = {item['status']: item['count'] for item in status_counts}
    
    # Get specific counts
    total_orders = Order.objects.count()
    pending_orders = status_dict.get('pending', 0)
    confirmed_orders = status_dict.get('confirmed', 0)
    processing_orders = status_dict.get('processing', 0)
    shipped_orders = status_dict.get('shipped', 0)
    delivered_orders = status_dict.get('delivered', 0)
    cancelled_orders = status_dict.get('cancelled', 0)
    refunded_orders = status_dict.get('refunded', 0)
    
    # Verify total matches (for debugging)
    calculated_total = (pending_orders + confirmed_orders + processing_orders + 
                       shipped_orders + delivered_orders + cancelled_orders + refunded_orders)
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'refunded_orders': refunded_orders,
        'recent_orders': recent_orders,
        'calculated_total': calculated_total,  # For verification
        'status_breakdown': status_dict,  # For debugging if needed
    }
    
    return render(request, 'orders/admin/dashboard.html', context)


@login_required
def get_pending_orders_count(request):
    """Get count of pending orders for admin notifications"""
    if not request.user.is_staff:
        return JsonResponse({'count': 0})
    
    pending_count = Order.objects.filter(status='pending').count()
    return JsonResponse({'count': pending_count})
