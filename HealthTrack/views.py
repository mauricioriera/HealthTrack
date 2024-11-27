from django.contrib.auth import logout as do_logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render


def inicio(request):
    context = {'foo': 'bar'}
    return render(request, 'index.html', context)

def crear_usuario(request):
    return render(request,'crear_usuario.html')


def logout(request):
    do_logout(request)
    return redirect('inicio')


class CustomLoginView(LoginView):
    def form_valid(self, form):
        super().form_valid(form)
        user = self.request.user
        if (hasattr(user, 'profesionalsalud') and user.profesionalsalud.groups.name == "Profesional_Salud"):
            return redirect('principal_paciente')
        elif (hasattr(user, 'paciente') and user.paciente.groups.name == "Paciente"):
            return redirect('principal_paciente')
        else:
            return redirect('logout')

def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {}, status=403)