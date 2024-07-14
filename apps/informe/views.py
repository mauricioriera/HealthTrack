from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.informe.forms import informeForm
from apps.informe.models import informe
from django.contrib import messages



class InformeCrear(CreateView):
    model = informe
    form_class = informeForm
    template_name = 'informe/informe_add.html'
    success_url = reverse_lazy('inicio')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.save()
            paciente= informe.paciente
            paciente.save()
            messages.add_message(request, messages.SUCCESS, 'Su informe se cargo correctamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, 'Su informe no se cargo')
            return render(request, self.template_name, {'form': form})