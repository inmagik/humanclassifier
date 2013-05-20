from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet


from .models import Plant, PlantImage, ReferencePlant, ReferencePlantImage
from .forms import PlantForm, PlantImageFormSet, JudgementForm


from judgements.models import Judgement



class PlantImageInline(InlineFormSet):
    model = PlantImage
    

class PlantCreate(CreateWithInlinesView):
    model = Plant
    form_class = PlantForm
    inlines = [PlantImageInline]
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlantCreate,self).dispatch(*args, **kwargs)
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PlantCreate, self).form_valid(form)
        
  
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
        if self.request.user.is_authenticated():
            qset = self.object.judgements_for_field("plant_name", user=self.request.user)
            context['user_judgements'] = qset
            
        else:
            context['user_judgements'] = []
            context['user_judgements_form'] = "No form here. link to login"
        return context
    

class ReferencePlantList(ListView):
    model = ReferencePlant
    

class ReferencePlantDetail(DetailView):
    model = ReferencePlant
    
    def get_context_data(self, **kwargs):
        context = super(ReferencePlantDetail, self).get_context_data(**kwargs)
        context['pictures'] = ReferencePlantImage.objects.filter(reference_plant=self.object)
        return context



    
    
    
class JudgementCreate(CreateView):
    model = Judgement
    form_class = JudgementForm
    template_name = "plants/judgement_form.html"
    fieldname = "plant_name"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.plant = get_object_or_404(Plant, pk=kwargs['pk'])
        return super(JudgementCreate, self).dispatch(*args, **kwargs)
        

    def get_success_url(self):
        return reverse("plant_detail", args=(self.plant.id,))

    def get_context_data(self, *args, **kwargs):

        context_data = super(JudgementCreate, self).get_context_data(
            *args, **kwargs)
        context_data.update({'plant' : self.plant , 'fieldname' : self.fieldname })
        return context_data
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.content_object = self.plant
        self.object.fieldname = self.fieldname
        self.object.save()
        return super(JudgementCreate, self).form_valid(form)