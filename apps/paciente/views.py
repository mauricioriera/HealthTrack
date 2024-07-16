from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from apps.paciente.forms import pacienteForm, RegistroForm
from apps.paciente.models import paciente
from django.contrib import messages


class PacienteCrear(CreateView):
    model = paciente
    form_class = pacienteForm
    second_form_class = RegistroForm
    template_name = 'paciente/paciente_add.html'
    success_url = reverse_lazy('inicio')

    def get_context_data(self, **kwargs):
        context = super(PacienteCrear, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
            return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            paciente = form.save(commit=False)
            paciente.user = form2.save()
            g = Group.objects.get(name='Paciente')
            paciente.groups = g
            g.user_set.add(paciente.user)
            paciente.save()
            messages.add_message(request, messages.SUCCESS, 'Su perfil se creo correctamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, 'Su perfil no se pudo crear')
            return render(request, self.template_name, {'form': form, 'form2': form2})