from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from apps.paciente.models import paciente
from apps.profesional_salud.decorator import profesional_salud_required


@login_required
def prueba(request):
    return render(request,'test.html',{})

@login_required
def vista_pincipal_ps(request):
    usuario = request.user
    context = {
        'usuario ': usuario
    }
    return render(request,'profesional_salud/principal.html', context)

@login_required
def seleccion_paciente(request):
    pacient = paciente.objects.all()
    return render(request, 'profesional_salud/paciente_seleccion.html', {'paciente': pacient})
def procesar_paciente(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('user_id')
        return redirect(reverse('lista_archivos', args=[paciente_id]))

    return HttpResponse("Método no permitido", status=405)