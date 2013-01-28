from django import forms
from .models import Plant



class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        exclude = ('user', 'accepted', 'offensive', 'plant_name',)