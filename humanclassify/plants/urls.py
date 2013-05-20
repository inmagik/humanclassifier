# urls.py
from django.conf.urls import patterns, url
from .views import ( 
        PlantCreate, PlantUpdate, PlantDelete, PlantList, PlantDetail, 
        JudgementCreate,
        ReferencePlantList, ReferencePlantDetail,
    )

urlpatterns = patterns('',
    # ...
    
    url(r'plant/reference_plants/$', ReferencePlantList.as_view(), name='reference_plant_list'),
    url(r'plant/reference_plant/(?P<pk>\d+)/$', ReferencePlantDetail.as_view(), name='reference_plant_detail'),
    
    url(r'plant/add/$', PlantCreate.as_view(), name='plant_add'),
    url(r'plant/(?P<pk>\d+)/edit/$', PlantUpdate.as_view(), name='plant_update'),
    url(r'plant/(?P<pk>\d+)/delete/$', PlantDelete.as_view(), name='plant_delete'),
    
    url(r'plants/$', PlantList.as_view(), name='plant_list'),
    url(r'plant/(?P<pk>\d+)/$', PlantDetail.as_view(), name='plant_detail'),
    url(r'plant/(?P<pk>\d+)/judgement/add/$', JudgementCreate.as_view(), name='judgement_add'),
    
    
    
    
)