from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
