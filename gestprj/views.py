from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from gestprj.models import Projectes
from gestprj.forms import UsuariXarxaForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def list_projectes(request):
    llista_projectes = Projectes.objects.all()
    context = { 'llista_projectes' : llista_projectes }
    return render(request,'gestprj/llista_projectes.html',context)

def new_project(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UsuariXarxaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UsuariXarxaForm()

    return render(request, 'gestprj/projecte_nou.html', {'form': form})