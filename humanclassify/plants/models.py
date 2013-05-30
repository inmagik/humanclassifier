from django.db import models
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from judgements.models import OpinionatedModel, JudgementModel
from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType


class PlantJudgement(JudgementModel):
    plant_name = models.CharField(max_length=256, blank=False)
    motivation = models.TextField(default='')


class Plant(OpinionatedModel):

    opinionated_fields = ['plant_name']
    judgement_models ={ 'PlantJudgement' : PlantJudgement}
    plant_name = models.CharField(max_length=256, null=True, blank=True)

    suggested_plant_name = models.CharField(max_length=256, null=True, blank=True)
    notes = models.TextField(null=True, blank=True, help_text="Enter some optional notes about this plant.")
    location_description = models.TextField(null=True, blank=True, help_text="Enter some optional description of the place where the plant lives")
    
    
    #def clean(self):
    #    if not self.pictures.count():
    #        raise ValidationError('Must set pictures')
    
    
    def save(self, *args, **kwargs):
        print args, kwargs
        return super(Plant, self).save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.pk})
        
    def get_plant_judgements(self):
        c_type = ContentType.objects.get_for_model(self)
        qset = PlantJudgement.objects.filter(content_type = c_type, object_id = self.pk)
        return qset
    



class PlantImage(models.Model):

    plant = models.ForeignKey(Plant, related_name="pictures")
    picture = ImageField(upload_to='plants')
    
    @property
    def img_url(self):
        return self.picture.url 
    
    
class ReferencePlant(models.Model):
    
    name = models.CharField(max_length=256)
    
    ordo = models.CharField(max_length=256, blank=True, null=True)
    unranked_classis = models.CharField(max_length=256, blank=True, null=True)
    unranked_divisio = models.CharField(max_length=256, blank=True, null=True)
    regnum = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    binomial = models.CharField(max_length=256, blank=True, null=True)
    familia = models.CharField(max_length=256, blank=True, null=True)
    genus = models.CharField(max_length=256, blank=True, null=True)
    unranked_ordo = models.CharField(max_length=256, blank=True, null=True)
    species = models.CharField(max_length=256, blank=True, null=True)
    synonyms = models.CharField(max_length=256, blank=True, null=True)
    binomial_authority = models.CharField(max_length=256, blank=True, null=True)
        
    wiki_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    wiki_content = models.TextField(blank=True, default='', null=True)
    
    
    def get_thumb(self, image):
        im = get_thumbnail(image, '100x100', crop='center', quality=99)
        return im.url
    
    
    @property
    def first_image(self):
        if self.images.count:
            first_img = self.images.all()[0]
            img = first_img.image
            return self.get_thumb(img)
        return null
    
    @property
    def all_images(self):
        if self.images.count:
            return  [ self.get_thumb(x.image) for x in self.images.all()[:10]]
        return []
        
    
    def get_absolute_url(self):
        return reverse('reference_plant_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u'%s' % self.name
        
        
    class Meta:
        ordering = ['name', 'genus']
        

class ReferencePlantImage(models.Model):

    reference_plant = models.ForeignKey(ReferencePlant, related_name="images")
    image = ImageField(null=True, upload_to="reference_images")
    


#from django.db.models.signals import pre_save
#from django.dispatch import receiver

#@receiver(pre_save, sender=Plant)
#def check_image_requirement(sender, instance, **kwargs):
#    if instance.pictures.count() == 0:
#        raise ValidationError("Listing is required to have at least one image") 