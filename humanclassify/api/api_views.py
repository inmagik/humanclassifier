from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import (
     UserSerializer, GroupSerializer, 
     ReferencePlantSerializer, ReferencePlantImageSerializer,
     PlantSerializer, PlantImageSerializer,
     
)

from plants.models import ReferencePlant, ReferencePlantImage, Plant, PlantImage

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    
    
class ReferencePlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reference plants to be viewed or edited.
    """
    queryset = ReferencePlant.objects.all()
    serializer_class = ReferencePlantSerializer


class ReferencePlantImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ReferencePlantImage.objects.all()
    serializer_class = ReferencePlantImageSerializer
    
class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class PlantImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PlantImage.objects.all()
    serializer_class = PlantImageSerializer
