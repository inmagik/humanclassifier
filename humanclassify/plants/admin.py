from django.contrib import admin

from .models import Plant, PlantImage, ReferencePlant, ReferencePlantImage

admin.site.register(Plant)
admin.site.register(PlantImage)
admin.site.register(ReferencePlant)
admin.site.register(ReferencePlantImage)