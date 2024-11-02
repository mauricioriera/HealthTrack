import os
from datetime import timedelta, datetime

import magic
from apscheduler.schedulers.background import BackgroundScheduler
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore, register_job

from apps.informe.forms import InformeForm, DesencriptarArchivoForm
from apps.informe.models import Informe
from apps.informe.models import InformeTemporal, Solicitud
from apps.paciente.decorator import paciente_required
from apps.paciente.models import Paciente
from apps.profesional_salud.decorator import profesional_salud_required
from apps.profesional_salud.models import ProfesionalSalud
from apps.profesional_salud.utils import EstadoSolicitud

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(limpiar_tabla_temporal, 'interval', minutes=5)
    scheduler.start()


def limpiar_tabla_temporal():
    print("Scheduler limpiar_tabla_temporal ejecutando...")
    solicitudes_aceptadas=Solicitud.objects.filter(estado=EstadoSolicitud.ACEPTADA.value)

    for solicitud in solicitudes_aceptadas:
        tiempo_expiracion = solicitud.fecha_creacion + timedelta(minutes=solicitud.tiempo_de_vida)
        esta_expirado = timezone.now() > tiempo_expiracion
        if esta_expirado:
            solicitud.estado=EstadoSolicitud.VENCIDA.value
            solicitud.save()

            paciente_id = solicitud.paciente.id
            profesional_id = solicitud.profesional_salud.id
            informes_a_eliminar = InformeTemporal.objects.filter(paciente_id=paciente_id,
                                                                profesional_salud_id=profesional_id)
            count, _ = informes_a_eliminar.delete()

            print(f"Se eliminaron {count} informes temporales de la solicitud.")

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
    return desencriptar_archivos(request, paciente_id)

def desencriptar_archivos(request,paciente_id):


    if request.method == 'POST':
        form= DesencriptarArchivoForm(request.POST)
        if form.is_valid():
            informes = Informe.objects.filter(paciente_id=paciente_id).order_by('-fecha_informe')
            informe_a_validar = informes.first()

            llave_privada=form.cleaned_data['llave']

            if llave_privada_no_es_valida(informe_a_validar, llave_privada):
                return render(request, 'informe/error_clave_privada.html')

            request.session['llave_privada'] = llave_privada
            return render(request, 'informe/lista_archivos.html',{'informes': informes})
    else:
        form= DesencriptarArchivoForm()
    return render(request, 'informe/desencriptar_archivo.html',{'form':form})

@profesional_salud_required()
@login_required
def lista_archivos_profesional(request, paciente_id):

    profesional_id = request.user.profesionalsalud.id

    try:
        solicitud = Solicitud.objects.get(profesional_salud = profesional_id, paciente = paciente_id, estado = EstadoSolicitud.ACEPTADA.value)
    except:
        return render(request, 'profesional_salud/error_expiracion.html')

    tiempo_expiracion = solicitud.fecha_creacion + timedelta(minutes=solicitud.tiempo_de_vida)
    esta_expirado = timezone.now() > tiempo_expiracion

    if esta_expirado:
        return render(request, 'profesional_salud/error_expiracion.html')


    tiempo_segundos = solicitud.tiempo_de_vida * 60

    tiempo_mili = tiempo_segundos * 1000

    if request.method == 'POST':
        form= DesencriptarArchivoForm(request.POST)
        if form.is_valid():
            informes = InformeTemporal.objects.filter(paciente_id=paciente_id, profesional_salud_id=profesional_id)
            informe_a_validar = informes.first()

            llave_privada=form.cleaned_data['llave']

            if llave_privada_no_es_valida(informe_a_validar, llave_privada):
                return render(request, 'informe/error_clave_privada.html')

            request.session['llave_privada_profesional'] = llave_privada

            return render(request, 'informe/lista_archivos.html',{'informes': informes, 'tiempo': tiempo_mili})
    else:
        form= DesencriptarArchivoForm()
    return render(request, 'informe/desencriptar_archivo.html',{'form': form})


def mostrar_archivo_paciente(request, archivo_id):
    informe = get_object_or_404(Informe, id=archivo_id)

    llave_aes = desencriptar_llave_aes_con_rsa(informe.llave_simetrica_encriptada, request.session.get('llave_privada'))
    informe_desencriptado = desencriptar_informe_con_llave_aes(llave_aes, informe.archivo)

    mime = magic.Magic(mime=True)
    content_type = mime.from_buffer(informe_desencriptado)

    response = HttpResponse(informe_desencriptado, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="informe"'
    return response

def mostrar_archivo_profesional(request, archivo_id):
    informe = get_object_or_404(InformeTemporal, id=archivo_id)

    llave_aes = desencriptar_llave_aes_con_rsa(informe.llave_simetrica_encriptada, request.session.get('llave_privada_profesional'))
    informe_desencriptado = desencriptar_informe_con_llave_aes(llave_aes, informe.archivo)

    mime = magic.Magic(mime=True)
    content_type = mime.from_buffer(informe_desencriptado)

    response = HttpResponse(informe_desencriptado, content_type=content_type)
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
def desencriptar_llave_aes_con_rsa(llave_simetrica_encriptada,llave_privada_str):
    llave_privada = cargar_llave_privada(llave_privada_str)
    llave_aes=llave_privada.decrypt(
        llave_simetrica_encriptada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return llave_aes
def desencriptar_informe_con_llave_aes(llave_aes, archivo):
    iv=archivo[:16]
    datos_desencriptados=archivo[16:]
    cipher= Cipher(algorithms.AES(llave_aes),modes.CFB(iv),backend=default_backend())
    decryptor= cipher.decryptor()

    datos_desencriptados= decryptor.update(datos_desencriptados) + decryptor.finalize()
    return datos_desencriptados

def cargar_llave_privada(clave):
    return serialization.load_pem_private_key(
        clave.encode(),
        password=None,
    )

def llave_privada_no_es_valida(informe_a_validar, llave_privada):
    if informe_a_validar is not None:
        try:
            llave_aes = desencriptar_llave_aes_con_rsa(informe_a_validar.llave_simetrica_encriptada, llave_privada)
            desencriptar_informe_con_llave_aes(llave_aes, informe_a_validar.archivo)
        except:
            return True
    else:
        try:
            cargar_llave_privada(llave_privada)
        except:
            return True
    return False