from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def centro_medico(request):
    return render(request, 'base/base.html', {
    })
