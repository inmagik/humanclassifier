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
    
