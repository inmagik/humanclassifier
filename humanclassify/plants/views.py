from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Plant
from .forms import PlantForm

class PlantCreate(CreateView):
    form_class = PlantForm
    model = Plant
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PlantCreate, self).form_valid(form)

class PlantUpdate(UpdateView):
    form_class = PlantForm
    model = Plant

class PlantDelete(DeleteView):
    model = Plant
    success_url = reverse_lazy('author-list')