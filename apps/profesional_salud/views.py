from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from apps.informe.forms import TiempoForm
from apps.paciente.models import Paciente
from apps.profesional_salud.decorator import profesional_salud_required
import base64
from apps.profesional_salud.forms import ProfesionalSaludform, RegistroForm
from apps.profesional_salud.models import ProfesionalSalud


class principal(ListView):
    model = Paciente
    template_name = 'profesional_salud/principal.html'
    context_object_name = 'pacientes'


@profesional_salud_required()
@login_required
def solicita_acceso(request, paciente_id):
    paciente_resultado = get_object_or_404(Paciente, id=paciente_id)
    id_profesional = request.user.id
    link_aceptar = f"{settings.SITE_URL}/paciente/aceptar_solicitud/{id_profesional}/{paciente_resultado.id}"
    enviar_mail_paciente(paciente_resultado.user.email, link_aceptar, request.user.username)

    messages.success(request, 'Solicitud de acceso enviada correctamente.')

    return redirect('principal')


def enviar_mail_paciente(paciente_email, link_aceptar, username):
    send_mail(
        'Solicitud de acceso a sus archivos',
        f'El médico {username} ha solicitado acceso a tus archivos. Por favor, ingrese al siguiente link: {link_aceptar}',
        settings.EMAIL_HOST_USER,
        [paciente_email],
        fail_silently=False,
    )


def permitir_acceso(request, user_id, paciente_id, tiempo_acceso):
    link = generar_magic_link(paciente_id, tiempo_acceso)
    profesional = get_object_or_404(User, id=user_id)
    enviar_magic_link(profesional.email, link)
    return render(request, 'registration/login.html')

def solicitar_tiempo_acceso(request, user_id, paciente_id):
    if request.method == "POST":
        form = TiempoForm(request.POST)
        if form.is_valid():

            return permitir_acceso(request, user_id, paciente_id, form.cleaned_data['duracion_permiso'])

    else:
        form = TiempoForm()

    return render(request, "profesional_salud/solicitar_tiempo.html", {"form": form})

def generar_magic_link(paciente_id, tiempo_acceso):
    signer = TimestampSigner()
    token = signer.sign(paciente_id)
    tiempo_codificado = base64.b64encode(tiempo_acceso.to_bytes(2, byteorder='big'))
    tiempo_final = tiempo_codificado.decode('utf-8')
    link = f"{settings.SITE_URL}/informe/lista/profesional/{token}/{tiempo_final}"
    return link


def enviar_magic_link(profesional_email, link):
    send_mail(
        'Solicitud de acceso a sus archivos',
        f'El usuario le dio acceso a sus archivos. Por favor, haga clic en el siguiente enlace para verlos: {link}',
        settings.EMAIL_HOST_USER,
        [profesional_email],
        fail_silently=False,
    )


def eviar_mail_denegado(request, user_id, paciente_id):
    paciente_encontrado = get_object_or_404(Paciente, id=paciente_id)
    profesional = get_object_or_404(User, id=user_id)
    send_mail(
        'Solicitud de acceso a sus archivos',
        f'El usuario {paciente_encontrado.user.first_name}.{paciente_encontrado.user.last_name} no permitió acceso a sus archivos.',
        settings.EMAIL_HOST_USER,
        [profesional.email],
        fail_silently=False,
    )
    return render(request, 'profesional_salud/principal.html')

class ProfesionalCrear(CreateView):
    model = ProfesionalSalud
    form_class = ProfesionalSaludform
    second_form_class = RegistroForm
    template_name = 'profesional_salud/profesional_add.html'
    success_url = reverse_lazy('inicio')

    def get_context_data(self, **kwargs):
        context = super(ProfesionalCrear, self).get_context_data(**kwargs)
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
            profesional_salud = form.save(commit=False)
            profesional_salud.user = form2.save()
            g = Group.objects.get(name='Profesional_Salud')
            profesional_salud.groups = g
            g.user_set.add(profesional_salud.user)
            profesional_salud.save()
            messages.add_message(request, messages.SUCCESS, 'Su perfil se creo correctamente')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.add_message(request, messages.ERROR, 'Su perfil no se pudo crear')
            return render(request, self.template_name, {'form': form, 'form2': form2})
