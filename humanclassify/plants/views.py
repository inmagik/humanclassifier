from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet


from .models import Plant, PlantImage
from .forms import PlantForm, PlantImageFormSet



class PlantImageInline(InlineFormSet):
    model = PlantImage
    

class PlantCreate(CreateWithInlinesView):
    model = Plant
    form_class = PlantForm
    inlines = [PlantImageInline]
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlantCreate,self).dispatch(*args, **kwargs)
  
class PlantUpdate(UpdateWithInlinesView):
    model = Plant
    form_class = PlantForm
    template_name = "plants/plant_form_update.html"
    inlines = [PlantImageInline]
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlantUpdate,self).dispatch(*args, **kwargs)


class PlantDelete(DeleteView):
    model = Plant
    success_url = reverse_lazy('plant_list')
    
    @method_decorator(login_required)
    def dispatch(request, *args, **kwargs):
        return super(PlantCreate, self).dispatch(*args, **kwargs)


class PlantList(ListView):
    model = Plant
    

class PlantDetail(DetailView):
    model = Plant
    
    def get_context_data(self, **kwargs):
        context = super(PlantDetail, self).get_context_data(**kwargs)
        context['pictures'] = PlantImage.objects.filter(plant=self.object)
        return context
    
    