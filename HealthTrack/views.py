from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth import logout as do_logout




def inicio(request):
    context = {'foo': 'bar'}
    return render(request, 'index.html', context)

def logout(request):
    do_logout(request)
    return redirect('inicio')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user= self.request.user
        if(user.groups.filter(name="Profesional_Salud").exists()):
            return redirect('inicio')
        elif(user.groups.filter(name="Paciente").exists()):
            return redirect('prueba')
        else:
            return redirect('admin')



