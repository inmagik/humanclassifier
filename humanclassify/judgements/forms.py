from django import forms
from .models import Judgement


class JudgementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JudgementForm, self).__init__(*args, **kwargs)
        self.fields['motivation'].help_text = 'Optionally insert the motivation for your choice.'


    class Meta:
        model = Judgement
        exclude = ('user', 'content_object', 'object_id', 'content_type','fieldname')