from django import forms
from .models import Plant, PlantImage

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'jungle_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'jungle_type': forms.Select(attrs={'class': 'form-control'}),
        }

class PlantImageForm(forms.ModelForm):
    class Meta:
        model = PlantImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }