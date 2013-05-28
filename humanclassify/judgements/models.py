from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from jsonfield import JSONField



class UserSubmittedModel(models.Model):
    """
    """
    
    accepted = models.BooleanField(default=False)
    offensive = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True)
    
    class Meta:
        abstract = True


class OpinionatedModel(UserSubmittedModel):
    """
    """
    
    opinionated_fields = []
    judgement_models = {}
    judgements = generic.GenericRelation('judgements.Judgement')
    
    @property
    def is_complete(self):
        """
        """
        for fieldname in self.opinionated_fields:
            value = getattr(self, fieldname)
            #TODO: move to a setting or class config null values list
            if value in [None, '']:
                return False
        return True 
    
    
    def judgements_for_field(self, fieldname, user=None):
        qset = self.judgements.filter(fieldname=fieldname)
        if user:
            qset=qset.filter(user=user)
        return qset
        
    def get_judgements_model(self, key, user=None):
        if key not in self.judgement_models:
            return None
            
        mod = self.judgement_models[key]
        c_type = ContentType.objects.get_for_model(self)
        qset = mod.objects.filter(content_type = c_type, object_id = self.pk)
        
        if user:
            qset=qset.filter(user=user)
        return qset
        
    def get_judgements_models(self, user=None):
        out = {}
        for key in self.judgement_models:
            out[key] = self.get_judgements_model(key, user=user)
        return out
        
    def count_judgements_models(self):
        out = 0
        c_type = ContentType.objects.get_for_model(self)
        for key in self.judgement_models:
            mod = self.judgement_models[key]
            out += mod.objects.filter(content_type = c_type, object_id = self.pk).count()
        return out
    
    
    class Meta:
        abstract = True


class JudgementModel(models.Model):
    """
    Base class for linkable judgement model
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    user = models.ForeignKey(User)

    class Meta:
        abstract = True


class Judgement(models.Model):
    """
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    fieldname = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    value = JSONField() 
    motivation = models.TextField(null=True, blank=True)
    
