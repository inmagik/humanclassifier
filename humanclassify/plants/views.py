from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Plant, PlantImage
from .forms import PlantForm, PlantImageFormSet


class PlantCreate(CreateView):
    form_class = PlantForm
    model = Plant
    success_url = reverse_lazy("plant_list")
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlantCreate,self).dispatch(*args, **kwargs)
    
    """
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PlantCreate, self).form_valid(form)
    """ 
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        
        context = self.get_context_data()
        plantimage_form = context['plantimage_formset']
        print dir(plantimage_form)
        if plantimage_form.is_valid():
            print 1
            self.object = form.save()
            plantimage_form.instance = self.object
            plantimage_form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            print 2
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(PlantCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['plantimage_formset'] = PlantImageFormSet(self.request.POST)
        else:
            context['plantimage_formset'] = PlantImageFormSet()
        return context


class PlantUpdate(UpdateView):
    form_class = PlantForm
    model = Plant
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlantCreate,self).dispatch(*args, **kwargs)

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
        context['pictures'] = PlantImage.objects.all()
        print context
        return context
    
    