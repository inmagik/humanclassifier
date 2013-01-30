from urlparse import urlparse 
import urllib2 
from django.core.files import File
from django.core.files.base import ContentFile

from pymongo import MongoClient
from .models import ReferencePlant, ReferencePlantImage


HANDLED_FIELDS = ['ordo', 'binomial_authority', 'unranked_classis', 'unranked_divisio', 'regnum', 'url', 'binomial', 'familia', 'genus', 'unranked_ordo', 'species','synonyms']
IGNORED_IMAGES = ["Commons-logo.svg"]


def is_plant(obj):
    try:
        info = obj['info']
        regnum = info['regnum']
        if regnum.replace("[",'').replace("]",'').lower() == 'plantae':
            return True
    except:
        pass
    return False

        
def create_model_from_obj(obj):
    info = obj['info']
    page_title = obj['page_title']
    
    #for now we don't parse content, but it's there in any case
    #content = obj['content']
    
    model_kwargs = {}
    for fi in HANDLED_FIELDS:
        value = info.get(fi, None)
        if value is not None:
            value = value.replace(']', '').replace('[','').replace('"', '').replace("''", '')
        model_kwargs[fi] = value
    
    try:
        plant = ReferencePlant.objects.get(name=page_title).update(**model_kwargs)
    except:
        plant = ReferencePlant(name=page_title, **model_kwargs)
    
    plant.save()
    plant.images.all().delete()
    
    
    image_urls = []
    if 'images_info' in obj:
        images_info = obj['images_info']
        for image_info in images_info:
            try:
                url = image_info['imageinfo'][0]['url']
                filename = url.split('/')[-1]
                if filename not in IGNORED_IMAGES:
                    image_urls.append(url)
            except:
                pass
            
    if image_urls:
        for image_url in image_urls:
            
            name = urlparse(image_url).path.split('/')[-1]
            print "reading image %s" % image_url  
            content = ContentFile(urllib2.urlopen(image_url).read())
            img = ReferencePlantImage(reference_plant=plant)
            img.save()
            img.image.save(name, content, save=True)
    
    return plant
    
    
    


def import_plants_from_mongo(dbname, collectionname):
    connection = MongoClient()
    db = connection[dbname]
    collection = db[collectionname]
    objects = collection.find()
    
    for obj in objects:
        if is_plant(obj):
            p = create_model_from_obj(obj)
            #print "model saved", p.name
            