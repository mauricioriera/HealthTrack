import base64

import magic
from django.contrib.auth.decorators import login_required
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from apps.informe.forms import InformeForm
from apps.informe.models import Informe
from apps.paciente.decorator import paciente_required
from apps.paciente.models import Paciente
from apps.profesional_salud.decorator import profesional_salud_required
from apps.profesional_salud.models import ProfesionalSalud


@profesional_salud_required()
@login_required
def subir_archivo(request, profesional_id, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    if request.method == 'POST':
        form = InformeForm(request.POST, request.FILES)
        if form.is_valid():
            profesional = ProfesionalSalud.objects.get(id=profesional_id)
            archivo = form.cleaned_data['archivo']
            titulo = form.cleaned_data['titulo']
            fecha_informe= form.cleaned_data['fecha_informe']

            # Lee el archivo y conviértelo a binario
            archivo_binario = archivo.read()

            # Guarda el archivo en la base de datos
            Informe.objects.create(
                paciente=paciente,
                profesional_salud=profesional,
                titulo=titulo,
                archivo=archivo_binario,
                fecha_informe=fecha_informe,
            )
            return redirect('principal')  # Redirige a una página de lista o de éxito
    else:
        form = InformeForm()
    return render(request, 'informe/informe_add.html', {'form': form, "paciente": paciente})


@paciente_required()
@login_required
def lista_archivos_paciente(request, paciente_id):
    archivos = Informe.objects.filter(paciente_id=paciente_id).order_by('-fecha_informe')
    return render(request, 'informe/lista_archivos.html', {'archivos': archivos})


@profesional_salud_required()
@login_required
def lista_archivos_profesional(request, token, tiempo_codificado):
    signer = TimestampSigner()
    tiempo_bytes = base64.b64decode(tiempo_codificado)
    tiempo = int.from_bytes(tiempo_bytes, byteorder='big') * 60
    try:
        paciente_id = signer.unsign(token, max_age=tiempo)
    except SignatureExpired:
        return render(request, 'profesional_salud/error_expiracion.html')
    except BadSignature:
        return render(request, 'profesional_salud/error_enlace.html')

    archivos = Informe.objects.filter(paciente_id=paciente_id)
    tiempo_mili = tiempo * 1000
    return render(request, 'informe/lista_archivos.html', {'archivos': archivos,'tiempo': tiempo_mili})



def mostrar_archivo(request, archivo_id):
    archivo = get_object_or_404(Informe, id=archivo_id)

    # Usa python-magic para detectar el tipo MIME del archivo
    mime = magic.Magic(mime=True)
    content_type = mime.from_buffer(archivo.archivo)

    response = HttpResponse(archivo.archivo, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="informe"'
    return response
