import base64
import os

import magic
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
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
            llave_aes = generar_llave_aes()
            llave_aes_con_rsa = encriptar_llave_aes_con_rsa(llave_aes, cargar_llave_publica(paciente.llave_publica))
            archivo_encriptado = encriptar_archivo_con_aes(archivo_binario, llave_aes)

            # Guarda el archivo en la base de datos
            Informe.objects.create(
                paciente=paciente,
                profesional_salud=profesional,
                titulo=titulo,
                archivo=archivo_encriptado,
                fecha_informe=fecha_informe,
                llave_simetrica_encriptada=llave_aes_con_rsa
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


def generar_llave_aes():
    return os.urandom(32)
def encriptar_llave_aes_con_rsa(llave_aes,llave_publica):
    llave_encriptada= llave_publica.encrypt(
        llave_aes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return  llave_encriptada
def encriptar_archivo_con_aes(contenido_archivo,llave_aes):
    iv=os.urandom(16)
    cipher=Cipher(algorithms.AES(llave_aes),modes.CFB(iv),backend=default_backend())
    encriptador= cipher.encryptor()
    datos_encriptados= encriptador.update(contenido_archivo)+ encriptador.finalize()
    return iv+datos_encriptados

def cargar_llave_publica(llave_publica):
    llave_publica_obj=serialization.load_pem_public_key(
        llave_publica.encode('utf-8'),
        backend=default_backend()
    )
    return llave_publica_obj