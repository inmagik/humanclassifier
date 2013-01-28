# urls.py
from django.conf.urls import patterns, url
from .views import PlantCreate, PlantUpdate, PlantDelete

urlpatterns = patterns('',
    # ...
    url(r'plant/add/$', PlantCreate.as_view(), name='plant_add'),
    url(r'plant/(?P<pk>\d+)/$', PlantUpdate.as_view(), name='plant_update'),
    url(r'plant/(?P<pk>\d+)/delete/$', PlantDelete.as_view(), name='plant_delete'),
)