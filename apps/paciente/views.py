from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from apps.paciente.decorator import paciente_required
from apps.paciente.forms import Pacienteform, RegistroForm
from apps.paciente.models import Paciente
from django.contrib import messages


class PacienteCrear(CreateView):
    model = Paciente
    form_class = Pacienteform
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
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            paciente.llave_publica = public_pem.decode('utf-8')
            paciente.save()
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            messages.add_message(request, messages.SUCCESS, 'Su perfil se creó correctamente.')
            return render(request, self.template_name, {
                'form': form,
                'form2': form2,
                'private_key': private_pem.decode('utf-8')
            })

        else:
            messages.add_message(request, messages.ERROR, 'Su perfil no se pudo crear')
            return render(request, self.template_name, {'form': form, 'form2': form2})
@paciente_required()
@login_required
def aceptar_solicitud(request,medico_id, paciente_id):
    context={'medico_id':medico_id, 'paciente_id':paciente_id}
    return render(request,'paciente/aceptar_solicitud.html', context)