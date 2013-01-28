from django.db import models
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from judgements.models import OpinionatedModel

class Plant(OpinionatedModel):

    opinionated_fields = ['plant_name']
    
    picture = models.ImageField(upload_to='plants')
    plant_name = models.CharField(max_length=256, null=True, blank=True)
    suggested_plant_name = models.CharField(max_length=256, null=True, blank=True)
    
    
    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.pk})
    
