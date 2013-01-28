# urls.py
from django.conf.urls import patterns, url
from .views import PlantCreate, PlantUpdate, PlantDelete, PlantList, PlantDetail

urlpatterns = patterns('',
    # ...
    url(r'plant/add/$', PlantCreate.as_view(), name='plant_add'),
    url(r'plant/(?P<pk>\d+)/edit/$', PlantUpdate.as_view(), name='plant_update'),
    url(r'plant/(?P<pk>\d+)/delete/$', PlantDelete.as_view(), name='plant_delete'),
    url(r'plant/$', PlantList.as_view(), name='plant_list'),
    url(r'plant/(?P<pk>\d+)/$', PlantDetail.as_view(), name='plant_detail'),
    
)