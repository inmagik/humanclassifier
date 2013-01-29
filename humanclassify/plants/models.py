from django.db import models
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from judgements.models import OpinionatedModel
from sorl.thumbnail import ImageField


class Plant(OpinionatedModel):

    opinionated_fields = ['plant_name']
    plant_name = models.CharField(max_length=256, null=True, blank=True)
    suggested_plant_name = models.CharField(max_length=256, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.pk})
    



class PlantImage(models.Model):

    plant = models.ForeignKey(Plant, related_name="pictures")
    picture = ImageField(upload_to='plants')