from django import forms
from django.forms.models import inlineformset_factory

from .models import Plant, PlantImage, PlantJudgement, ReferencePlant
from judgements.models import Judgement


class JudgementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JudgementForm, self).__init__(*args, **kwargs)
        self.fields['motivation'].help_text = 'Optionally insert the motivation for your choice.'


    class Meta:
        model = Judgement
        exclude = ('user', 'content_object', 'object_id', 'content_type','fieldname')


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        exclude = ('user', 'accepted', 'offensive', 'plant_name',)
        
                
PlantImageFormSet = inlineformset_factory(Plant, PlantImage, extra=4)



class PlantJudgementForm(forms.ModelForm):
    class Meta:
        model = PlantJudgement
        fields = ['plant_name']
        
    def __init__(self, *args, **kwargs):
        super(PlantJudgementForm, self).__init__(*args, **kwargs)
        self.fields['plant_name'] = forms.ChoiceField(choices=[ (o.name, o.name) for o in ReferencePlant.objects.all()])
