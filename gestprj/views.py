from django.shortcuts import render
from django.http import HttpResponse
from gestprj.models import Projectes

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def list_projectes(request):
    llista_projectes = Projectes.objects.all()
    context = { 'llista_projectes' : llista_projectes }
    return render(request,'gestprj/llista_projectes.html',context)
