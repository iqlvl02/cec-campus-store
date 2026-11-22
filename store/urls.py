from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.order_create, name='order_create'),
    path('success/', views.order_success, name='order_success'),
    path('track/', views.track_order, name='track_order'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('order/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('order/<int:order_id>/detail/', views.order_detail_json, name='order_detail_json'),
    path('verify-student/', views.verify_student, name='verify_student'),
    
]