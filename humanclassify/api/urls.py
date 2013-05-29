# urls.py
from django.conf.urls import patterns, url, include
    
import api_views
    
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
router.register(r'reference-plants', api_views.ReferencePlantViewSet)
router.register(r'reference-plant-images', api_views.ReferencePlantImageViewSet)
router.register(r'plants', api_views.PlantViewSet)
router.register(r'plant-images', api_views.PlantImageViewSet)


urlpatterns = patterns('',

    url(r'', include(router.urls)),
    
)