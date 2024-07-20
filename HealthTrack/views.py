from django.contrib.auth import logout as do_logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render


def inicio(request):
    context = {'foo': 'bar'}
    return render(request, 'index.html', context)


def logout(request):
    do_logout(request)
    return redirect('inicio')


class CustomLoginView(LoginView):
    def form_valid(self, form):
        super().form_valid(form)
        user = self.request.user
        if (hasattr(user, 'profesional_salud') and user.profesional_salud.groups.name == "Profesional_Salud"):
            return redirect('principal')
        elif (hasattr(user, 'paciente') and user.paciente.groups.name == "Paciente"):
            return redirect(('principal'))
        else:
            return redirect('centro_medico')
