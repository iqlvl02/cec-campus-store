from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student_id', 'full_name', 'item', 'specific_option', 'id_picture']
        widgets = {
            'student_id': forms.TextInput(attrs={'placeholder': 'XXXXXXX'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'id_picture': forms.FileInput(attrs={'accept': 'image/*'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specific_option'].required = False