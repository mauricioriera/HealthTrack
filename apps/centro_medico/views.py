from django.http import HttpResponse
from django.shortcuts import render


def centro_medico(request):
    return render(request, 'base/base.html', {
    })
