from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from apps.paciente.decorator import paciente_required
from apps.paciente.models import paciente
from apps.profesional_salud.decorator import profesional_salud_required


@login_required
def prueba(request):
    return render(request, 'test.html', {})



@login_required
def vista_pincipal_ps(request):
    usuario = request.user
    context = {
        'usuario ': usuario
    }
    return render(request, 'profesional_salud/principal.html', context)


@profesional_salud_required()
@login_required
def seleccion_paciente(request):
    pacient = paciente.objects.all()
    return render(request, 'profesional_salud/paciente_seleccion.html', {'paciente': pacient})


@profesional_salud_required()
@login_required
def procesar_paciente(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('user_id')
        return redirect(reverse('solicitar_acceso', args=[paciente_id]))
    return HttpResponse("Método no permitido", status=405)


@profesional_salud_required()
@login_required
def solicita_acceso(request, paciente_id):
    paciente_resultado = get_object_or_404(paciente, id=paciente_id)
    id_profesional = request.user.id
    link_aceptar = f"{settings.SITE_URL}/paciente/aceptar_solicitud/{id_profesional}/{paciente_resultado.id}"
    enviar_mail_paciente(paciente_resultado.user.email, link_aceptar, request.user.username)
    return render(request, 'profesional_salud/principal.html')


def enviar_mail_paciente(paciente_email, link_aceptar, username):
    send_mail(
        'Solicitud de acceso a sus archivos',
        f'El médico {username} ha solicitado acceso a tus archivos. Por favor, ingrese al siguiente link: {link_aceptar}',
        settings.EMAIL_HOST_USER,
        [paciente_email],
        fail_silently=False,
    )


def permitir_acceso(request, user_id, paciente_id):
    profesional = get_object_or_404(User, id=user_id)
    link = generar_magic_link(paciente_id)
    enviar_magic_link(profesional.email, link)
    return render(request, 'profesional_salud/principal.html')


def generar_magic_link(paciente_id):
    signer = TimestampSigner()
    token = signer.sign(paciente_id)
    link = f"{settings.SITE_URL}/profesional/acceso/{token}/"
    return link


def enviar_magic_link(profesional_email, link):
    send_mail(
        'Solicitud de acceso a sus archivos',
        f'El usurio le dio acceso a sus archivos. Por favor, haga clic en el siguiente enlace para verlos: {link}',
        settings.EMAIL_HOST_USER,
        [profesional_email],
        fail_silently=False,
    )


def verificar_magic_link(request, token):
    signer = TimestampSigner()
    try:
        paciente_id = signer.unsign(token, max_age=180)
    except SignatureExpired:
        return HttpResponseBadRequest('El enlace ha expirado.')
    except BadSignature:
        return HttpResponseBadRequest('El enlace no es válido.')

    # Guardar en la sesión que el acceso está permitido
    request.session['acceso_permitido'] = paciente_id
    return redirect('lista_archivos', paciente_id=paciente_id)
