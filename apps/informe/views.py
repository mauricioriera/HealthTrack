import magic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from apps.informe.forms import informeForm
from apps.informe.models import informe
from apps.profesional_salud.decorator import profesional_salud_required
from apps.profesional_salud.models import profesional_salud


@profesional_salud_required()
@login_required
def subir_archivo(request,profesional_id):
    if request.method == 'POST':
        form = informeForm(request.POST, request.FILES)
        if form.is_valid():
            paciente = form.cleaned_data['paciente']
            profesional = profesional_salud.objects.get(id=profesional_id)
            archivo = form.cleaned_data['archivo']
            titulo = form.cleaned_data['titulo']

            # Lee el archivo y conviértelo a binario
            archivo_binario = archivo.read()

            # Guarda el archivo en la base de datos
            informe.objects.create(
                paciente=paciente,
                profesional_salud=profesional,
                titulo=titulo,
                archivo=archivo_binario,
            )
            return redirect('principal')  # Redirige a una página de lista o de éxito
    else:
        form = informeForm()
    return render(request, 'informe/informe_add.html', {'form': form})


def lista_archivos(request, paciente_id):
    archivos = informe.objects.filter(paciente_id=paciente_id)
    return render(request, 'informe/lista_archivos.html', {'archivos': archivos})


def mostrar_archivo(request, archivo_id):
    archivo = get_object_or_404(informe, id=archivo_id)

    # Usa python-magic para detectar el tipo MIME del archivo
    mime = magic.Magic(mime=True)
    content_type = mime.from_buffer(archivo.archivo)

    response = HttpResponse(archivo.archivo, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="pepe"'
    return response
