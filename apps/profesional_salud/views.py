import os


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from django.views.generic import ListView, CreateView
from apps.informe.forms import AceptarSolicitudForm
from apps.informe.models import Informe, InformeTemporal, Solicitud
from apps.informe.views import llave_privada_no_es_valida
from apps.paciente.models import Paciente
from apps.profesional_salud.decorator import profesional_salud_required
from apps.profesional_salud.forms import ProfesionalSaludform, RegistroForm
from apps.profesional_salud.models import ProfesionalSalud
from apps.profesional_salud.utils import EstadoSolicitud

@profesional_salud_required()
@login_required
class principal(ListView):
    model = Paciente
    template_name = 'profesional_salud/principal.html'
    context_object_name = 'pacientes'

    def get_context_data(self, **kwargs):
        # Get the default context data
        context = super().get_context_data(**kwargs)

        # Query the pacientes queryset
        pacientes = context['pacientes']

        # Loop through each paciente and check if they have any associated files
        for paciente in pacientes:
            paciente.tiene_estudios = Informe.objects.filter(paciente_id=paciente.id).exists()

        # You can add more context variables as needed
        return context

@profesional_salud_required()
@login_required
def solicita_acceso(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    profesional_salud = get_object_or_404(ProfesionalSalud,id=request.user.profesionalsalud.id)
    solicitud_existente = Solicitud.objects.filter(Q(profesional_salud=profesional_salud.id) & Q(paciente=paciente.id)&
                                                   Q(estado=EstadoSolicitud.PENDIENTE.value)| Q(estado=EstadoSolicitud.ACEPTADA.value)).exists()


    if not solicitud_existente:
        Solicitud.objects.create(
            paciente=paciente,
            profesional_salud=profesional_salud,
            estado=EstadoSolicitud.PENDIENTE.value
        )
        messages.add_message(request, messages.SUCCESS, 'Solicitud enviada exitosamente')
    else:
        messages.add_message(request, messages.ERROR, 'Usted ya ha emitido una solicitud para este paciente')

    return redirect('principal')  # Redirige a la página del médico con las solicitudes

def solicitar_tiempo_acceso(request, user_id, paciente_id):
    if request.method == "POST":
        form = AceptarSolicitudForm(request.POST)
        if form.is_valid():
            request.session['llave_paciente']=form.cleaned_data['llave']
            return permitir_acceso(request, user_id, paciente_id, form.cleaned_data['duracion_permiso'])
    else:
        form = AceptarSolicitudForm()
    return render(request, "profesional_salud/solicitar_tiempo.html", {"form": form})

def permitir_acceso(request, user_id, paciente_id, tiempo_acceso):

    informes = Informe.objects.filter(paciente_id=paciente_id)
    profesional = ProfesionalSalud.objects.get(id=user_id)
    paciente = Paciente.objects.get(id=paciente_id)

    informe_a_validar=informes.first()
    if llave_privada_no_es_valida(informe_a_validar, request.session.get('llave_paciente')):
        return render(request, 'paciente/error_dar_acceso.html')

    for informe in informes:

        llave_aes = desencriptar_llave_aes_con_rsa(informe.llave_simetrica_encriptada, request.session.get('llave_paciente'))
        informe_desencriptado = desencriptar_informe_con_llave_aes(llave_aes, informe.archivo)

        llave_aes = generar_llave_aes()
        llave_aes_con_rsa = encriptar_llave_aes_con_rsa(llave_aes, cargar_llave_publica(profesional.llave_publica))
        archivo_encriptado = encriptar_archivo_con_aes(informe_desencriptado, llave_aes)

        InformeTemporal.objects.create(
            paciente=paciente,
            profesional_salud=profesional,
            titulo=informe.titulo,
            archivo=archivo_encriptado,
            fecha_informe=informe.fecha_informe,
            llave_simetrica_encriptada=llave_aes_con_rsa
        )

    profesional_id = profesional.id

    solicitud=Solicitud.objects.get(paciente=paciente_id, profesional_salud=profesional_id, estado=EstadoSolicitud.PENDIENTE.value)
    solicitud.estado=EstadoSolicitud.ACEPTADA.value
    solicitud.tiempo_de_vida=int(tiempo_acceso)
    solicitud.save()
    messages.add_message(request, messages.SUCCESS, 'Solicitud aceptada exitosamente')

    return render(request, 'paciente/principal_paciente.html')

def denegar_acceso(request, user_id, paciente_id):
    solicitud=Solicitud.objects.get(paciente=paciente_id, profesional_salud=user_id)
    solicitud.estado=EstadoSolicitud.RECHAZADA.value
    solicitud.save()
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
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            profesional_salud.llave_publica = public_pem.decode('utf-8')
            profesional_salud.save()
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

def desencriptar_llave_aes_con_rsa(llave_simetrica_encriptada,llave_paciente_str):
    llave_privada = cargar_llave_privada(llave_paciente_str)
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

@profesional_salud_required()
@login_required
def solicitudes(request):
    solicitudes = Solicitud.objects.filter(Q(profesional_salud=request.user.profesionalsalud.id) & (
                Q(estado=EstadoSolicitud.ACEPTADA.value) | Q(estado=EstadoSolicitud.RECHAZADA.value) | Q(
            estado=EstadoSolicitud.VENCIDA.value)))
    return render(request, 'profesional_salud/solicitudes_profesional.html', {'solicitudes': solicitudes})
