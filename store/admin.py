from django.contrib import admin
from django.utils.html import format_html
from .models import Order

admin.site.site_header = "CEC Campus Store Administration"
admin.site.site_title = "CEC Admin Portal"
admin.site.index_title = "Welcome to Cebu Eastern College Administration"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'course', 'year_level', 'item', 'quantity', 'total_amount', 'payment_status', 'order_status', 'id_picture_preview', 'created_at')
    list_filter = ('course', 'year_level', 'item', 'payment_method', 'payment_status', 'order_status', 'created_at')
    search_fields = ('full_name', 'student_id', 'course', 'payment_reference')
    readonly_fields = ('created_at', 'updated_at', 'total_amount', 'id_picture_preview')
    list_per_page = 25
    list_editable = ('order_status', 'payment_status')
    
    def id_picture_preview(self, obj):
        if obj.id_picture:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" />', obj.id_picture.url)
        return "No image"
    id_picture_preview.short_description = 'ID Picture'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_id', 'full_name', 'course', 'year_level'),
        }),
        ('Order Details', {
            'fields': ('item', 'specific_option', 'quantity', 'total_amount', 'notes'),
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'payment_reference'),
        }),
        ('Order Tracking', {
            'fields': ('order_status',),
        }),
        ('ID Picture', {
            'fields': ('id_picture', 'id_picture_preview'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_ready', 'mark_as_completed', 'mark_as_paid']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(order_status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed.')
    mark_as_confirmed.short_description = "Mark as Confirmed"
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(order_status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = "Mark as Processing"
    
    def mark_as_ready(self, request, queryset):
        updated = queryset.update(order_status='ready')
        self.message_user(request, f'{updated} orders ready for pickup.')
    mark_as_ready.short_description = "Mark as Ready for Pickup"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(order_status='completed')
        self.message_user(request, f'{updated} orders completed.')
    mark_as_completed.short_description = "Mark as Completed"
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payment_status='paid')
        self.message_user(request, f'{updated} orders marked as paid.')
    mark_as_paid.short_description = "Mark as Paid"