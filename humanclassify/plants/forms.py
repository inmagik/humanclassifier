from django import forms
from django.forms.models import inlineformset_factory

from .models import Plant, PlantImage



class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        exclude = ('user', 'accepted', 'offensive', 'plant_name',)
        
                
PlantImageFormSet = inlineformset_factory(Plant, PlantImage, extra=4)