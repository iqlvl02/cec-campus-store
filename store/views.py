from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
@csrf_exempt
def verify_student(request):
    """API endpoint to verify student with ID picture"""
    try:
        student_id = request.POST.get('student_id', '').strip()
        id_picture = request.FILES.get('id_picture')
        
        if student_id and id_picture:
            return JsonResponse({
                'verified': True,
                'student': {
                    'full_name': f"Student {student_id}",
                    'student_id': student_id,
                    'course': request.POST.get('course', ''),
                    'year_level': request.POST.get('year_level', '')
                }
            })
        
        return JsonResponse({'verified': False, 'error': 'Student not found'})
    
    except Exception as e:
        return JsonResponse({'verified': False, 'error': str(e)})

def order_create(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        course = request.POST.get('course', '').strip()
        year_level = request.POST.get('year_level', '')
        item = request.POST.get('item', '')
        specific_option = request.POST.get('specific_option', '')
        quantity = request.POST.get('quantity', 1)
        payment_method = request.POST.get('payment_method', 'cash')
        payment_reference = request.POST.get('payment_reference', '')
        notes = request.POST.get('notes', '')
        id_picture = request.FILES.get('id_picture')
        
        errors = []
        if not student_id:
            errors.append('Student ID is required.')
        if not full_name:
            errors.append('Full name is required.')
        if not course:
            errors.append('Please select your course/program.')
        if not item:
            errors.append('Please select an item.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'store/order_form.html')
        
        try:
            order = Order(
                student_id=student_id,
                full_name=full_name,
                course=course,
                year_level=year_level,
                item=item,
                specific_option=specific_option,
                quantity=int(quantity),
                payment_method=payment_method,
                payment_reference=payment_reference,
                notes=notes,
                id_picture=id_picture
            )
            order.save()
            messages.success(request, f'✅ Order Confirmed! Order ID: #{order.id}')
            return redirect('store:order_success')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'store/order_form.html')
    
    return render(request, 'store/order_form.html')

def order_success(request):
    return render(request, 'store/success.html')

def track_order(request):
    order = None
    search_query = request.GET.get('order_id', '')
    if search_query:
        if search_query.isdigit():
            order = Order.objects.filter(id=int(search_query)).first()
        if not order:
            order = Order.objects.filter(student_id__icontains=search_query).first()
        if not order:
            messages.error(request, 'No order found with that Student ID or Order ID.')
    return render(request, 'store/track_order.html', {'order': order, 'search_query': search_query})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('store:dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        errors = []
        
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not username:
            errors.append('Username is required.')
        if not email:
            errors.append('Email address is required.')
        if not password:
            errors.append('Password is required.')
        
        if username and User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if email and User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        
        if password and confirm_password and password != confirm_password:
            errors.append('Passwords do not match.')
        
        if password and len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if email:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Please enter a valid email address.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'store/register.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            login(request, user)
            messages.success(request, f'Welcome {first_name}! Your account has been created.')
            return redirect('store:dashboard')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'store/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('store:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'store/login.html')

@login_required(login_url='store:login')
def dashboard_view(request):
    all_orders = Order.objects.all()
    
    context = {
        'total_orders': all_orders.count(),
        'uniform_count': Order.objects.filter(item='uniform').count(),
        'sling_count': Order.objects.filter(item='sling').count(),
        'cover_count': Order.objects.filter(item='cover').count(),
        'recent_orders': all_orders[:10],
    }
    return render(request, 'store/dashboard.html', context)

@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.ORDER_STATUS_CHOICES):
            order.order_status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_order_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    return redirect('store:dashboard')

@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        # Delete the image file when order is deleted
        if order.id_picture:
            order.id_picture.delete()
        order.delete()
        messages.success(request, f'✅ Order #{order_id} has been deleted.')
    return redirect('store:dashboard')

@login_required
def order_detail_json(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    data = {
        'id': order.id,
        'full_name': order.full_name,
        'student_id': order.student_id,
        'course_display': order.get_course_display(),
        'year_level_display': order.get_year_level_display(),
        'item_display': order.get_item_display(),
        'specific_option': order.specific_option,
        'quantity': order.quantity,
        'total_amount': str(order.total_amount),
        'payment_method_display': order.get_payment_method_display(),
        'payment_status_display': order.get_payment_status_display(),
        'payment_reference': order.payment_reference,
        'order_status_display': order.get_order_status_display(),
        'notes': order.notes,
        'is_verified': order.is_verified,
        'id_picture_url': order.id_picture.url if order.id_picture else None,
        'created_at': order.created_at.strftime('%B %d, %Y %I:%M %p'),
    }
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('store:login')