from django.db import models

class Order(models.Model):
    ITEM_CHOICES = [
        ('uniform', 'School Uniform (₱850.00)'),
        ('sling', 'Sling ID (₱120.00)'),
        ('cover', 'ID Cover (₱50.00)'),
    ]
    
    COURSE_CHOICES = [
        ('BSED', 'Bachelor of Secondary Education'),
        ('BEED', 'Bachelor of Elementary Education'),
        ('BSHM', 'Bachelor of Science in Hospitality Management'),
        ('BSIT', 'Bachelor of Science in Information Technology'),
        ('BSCRIM', 'Bachelor of Science in Criminology'),
        ('SHS', 'Senior High School'),
    ]
    
    YEAR_LEVEL_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('grad', 'Graduate School'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash on Pickup'),
        ('gcash', 'GCash'),
        ('paymaya', 'PayMaya'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
    ]
    
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Student Details
    student_id = models.CharField('Student ID Number', max_length=20)
    full_name = models.CharField('Full Name', max_length=100)
    course = models.CharField('Course/Program', max_length=20, choices=COURSE_CHOICES, blank=True)
    year_level = models.CharField('Year Level', max_length=10, choices=YEAR_LEVEL_CHOICES, blank=True)
    
    # Order Details
    item = models.CharField('Item', max_length=20, choices=ITEM_CHOICES)
    specific_option = models.CharField('Option', max_length=50, blank=True)
    quantity = models.PositiveIntegerField('Quantity', default=1)
    
    # Payment Information
    payment_method = models.CharField('Payment Method', max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField('Payment Status', max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_reference = models.CharField('Payment Reference', max_length=100, blank=True)
    total_amount = models.DecimalField('Total Amount', max_digits=10, decimal_places=2, default=0)
    
    # Order Tracking
    order_status = models.CharField('Order Status', max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    notes = models.TextField('Additional Notes', blank=True)
    
    # ID Picture Field - ADD THIS
    id_picture = models.ImageField('ID Picture', upload_to='id_pictures/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_verified(self):
        """Check if student has uploaded ID picture"""
        return bool(self.id_picture)
    
    def __str__(self):
        return f"{self.full_name} - {self.get_item_display()}"
    
    def get_price(self):
        prices = {
            'uniform': 850.00,
            'sling': 120.00,
            'cover': 50.00,
        }
        return prices.get(self.item, 0) * self.quantity
    
    def save(self, *args, **kwargs):
        self.total_amount = self.get_price()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']