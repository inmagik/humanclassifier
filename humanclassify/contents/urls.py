# urls.py
from django.conf.urls import patterns, url
from .views import ( 
        HomePage, 
    )

urlpatterns = patterns('',
    # ...
    
    url(r'^$', HomePage.as_view(), name='home_page'),
    
)