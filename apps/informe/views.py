
from django.shortcuts import render, redirect
from apps.informe.forms import informeForm

def subir_archivo(request):
    if request.method == 'POST':
        form = informeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a una página de lista o de éxito
    else:
        form = informeForm()
    return render(request, 'informe/informe_add.html', {'form': form})