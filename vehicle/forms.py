from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    multiple_images = forms.FileField(
        required=False,
        widget=forms.FileInput()
    )
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'contract_number', 'multiple_images'] 
