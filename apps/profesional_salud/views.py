from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def lista(request):
    return render(request,'base/base.html',{})
@login_required
def prueba(request):
    return render(request,'test.html',{})
