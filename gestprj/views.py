from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from gestprj.models import Projectes
from gestprj.models import TUsuarisXarxa
from gestprj.forms import UsuariXarxaForm
from gestprj.forms import ProjectesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return HttpResponseRedirect('/menu/')
    # return HttpResponse("Hello, world.")
@login_required(login_url='/menu/')
def list_projectes(request):
    llista_projectes = TUsuarisXarxa.objects.all()
    context = { 'llista_projectes' : llista_projectes }
    return render(request,'gestprj/llista_projectes.html',context)

@login_required
def new_project(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectesForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectesForm()

    return render(request, 'gestprj/projecte_nou.html', {'form': form})

def login_view(request):
    username = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        print username, password

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print "Valid account"
        else:
            print "Inactive account"
    return render(request, 'gestprj/menu.html', {'username': username})

def logout_view(request):
    logout(request)
    return render(request, 'gestprj/menu.html', {'username': ""})