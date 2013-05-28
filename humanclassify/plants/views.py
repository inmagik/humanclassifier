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
from django.db.models import Count, Min, Sum, Avg

from .models import Plant, PlantImage, ReferencePlant, ReferencePlantImage, PlantJudgement
from .forms import PlantForm, PlantImageFormSet, JudgementForm, PlantJudgementForm


from judgements.models import Judgement
from django.forms.models import BaseInlineFormSet
from django.forms import ValidationError

class InvoiceOrderInlineFormset(BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise ValidationError('You must have at least one order')



class PlantImageInline(InlineFormSet):
    model = PlantImage
    formset_class = InvoiceOrderInlineFormset
    

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
    


class OpinionatedModelMixin(object):
    def get_context_data(self, **kwargs):
        context = super(OpinionatedModelMixin, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            qset = self.object.judgements_for_field("plant_name", user=self.request.user)
            context['user_judgements'] = qset
        else:
            context['user_judgements'] = []
        
        context['user_judgements_models'] = self.object.get_judgements_models(user=self.request.user.id)
        
        
        return context
    



class PlantDetail(OpinionatedModelMixin, DetailView):
    model = Plant
    
    def get_context_data(self, **kwargs):
        context = super(PlantDetail, self).get_context_data(**kwargs)
        context['judgements_models'] = self.object.get_plant_judgements()
        context['judgements_values'] = context['judgements_models'].values_list("plant_name").distinct().annotate(Count('plant_name'))
        return context
    

class ReferencePlantList(ListView):
    model = ReferencePlant
    

class ReferencePlantDetail(DetailView):
    model = ReferencePlant
    
    def get_context_data(self, **kwargs):
        context = super(ReferencePlantDetail, self).get_context_data(**kwargs)
        context['pictures'] = ReferencePlantImage.objects.filter(reference_plant=self.object)
        return context


class JudgementUpdate(UpdateView):
    pass
    
    
    
class JudgementCreate(CreateView):
    model = Judgement
    form_class = JudgementForm
    template_name = "plants/judgement_form.html"
    fieldname = "plant_name"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.plant = get_object_or_404(Plant, pk=kwargs['plant_pk'])
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
        


class JudgmentModelMixin(object):
    pass

        
class PlantJudgementCreate(CreateView):
    model = PlantJudgement
    form_class = PlantJudgementForm
    template_name = "plants/plant_judgement_form.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.plant = get_object_or_404(Plant, pk=kwargs['plant_pk'])
        return super(PlantJudgementCreate, self).dispatch(*args, **kwargs)
        

    def get_success_url(self):
        return reverse("plant_detail", args=(self.plant.id,))

    def get_context_data(self, *args, **kwargs):

        context_data = super(PlantJudgementCreate, self).get_context_data(
            *args, **kwargs)
        context_data.update({'plant' : self.plant })
        return context_data
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.content_object = self.plant
        self.object.save()
        return super(PlantJudgementCreate, self).form_valid(form)
        

#TODO: WE SHOULD MIXIN!!! plant should become "content_object"  
class PlantJudgementUpdate(UpdateView):
    model = PlantJudgement
    form_class = PlantJudgementForm
    template_name = "plants/plant_judgement_form.html"
    
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        #self.plant = get_object_or_404(Plant, pk=kwargs['plant_pk'])
        return super(PlantJudgementUpdate, self).dispatch(*args, **kwargs)
        

    def get_success_url(self):
        return reverse("plant_detail", args=(self.object.content_object.id,))

    def get_context_data(self, *args, **kwargs):

        context_data = super(PlantJudgementUpdate, self).get_context_data(
            *args, **kwargs)
        context_data.update({'plant' : self.object.content_object })
        return context_data
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        return super(PlantJudgementUpdate, self).form_valid(form)