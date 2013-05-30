from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.decorators import action


from plants.models import ReferencePlant, ReferencePlantImage, Plant, PlantImage

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ReferencePlantImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReferencePlantImage
        #fields = ('name', 'images')


class ReferencePlantSerializer(serializers.HyperlinkedModelSerializer):
    first_image = serializers.URLField(source='first_image', read_only=True)

    class Meta:
        model = ReferencePlant
        fields = ('name', 'first_image', 'id')
        
        
class PlantSerializer(serializers.HyperlinkedModelSerializer):

    @action()
    def approve(self, request, pk=None):
        plant = self.get_object()
        print plant
        return Response({'status': 'password set'})


    class Meta:
        model = Plant
        fields = ('plant_name', 'pictures')
        

class PlantImageSerializer(serializers.HyperlinkedModelSerializer):

    image_url = serializers.URLField(source='img_url', read_only=True)

    class Meta:
        model = PlantImage
        #fields = ['img_url']
        #fields = ('name', 'images')
