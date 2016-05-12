from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from gestprj.models import Projectes,TCategoriaPrj,TOrganismes
from gestprj.forms import UsuariXarxaForm
from gestprj.forms import ProjectesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from gestprj.utils import usuari_a_responsable

# Create your views here.
@login_required(login_url='/menu/')
def index(request):
    return HttpResponseRedirect('/welcome/')
    # return HttpResponse("Hello, world.")
@login_required(login_url='/menu/')
def list_projectes(request):
    # llista_projectes = TUsuarisXarxa.objects.all()
    # usuarixarxa = usuari_xarxa_a_user(request)
    responsable = usuari_a_responsable(request)

    if responsable is not None:
        llista_projectes = Projectes.objects.filter(id_resp__id_resp=responsable.id_resp)
    else:
        llista_projectes = None

    #llista_projectes = Projectes.objects.all()
    # for projecte in llista_projectes:
    #     if projecte.id_resp is not None:
    #         if projecte.id_resp.id_usuari is not None:
    #             print projecte.id_resp.id_usuari.nom_usuari
    context = { 'llista_projectes' : llista_projectes,'titulo':"LLISTA DE PROJECTES" }
    return render(request,'gestprj/llista_projectes.html',context)

@login_required(login_url='/menu/')
def new_project(request):
     # if this is a POST request we need to process the form data

    categories = TCategoriaPrj.objects.all()
    organismes = TOrganismes.objects.all()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # validez = 0
        form = ProjectesForm(request.POST)
        # form = ProjectesForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/welcome/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectesForm()

    return render(request, 'gestprj/projecte_nou.html', {'form': form,'titulo':'NOU PROJECTE', 'categories':categories, 'organismes':organismes})

def login_view(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        # print username, password

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/welcome/',{'username': username})
        else:
            return render(request, 'gestprj/menu.html', {'username': username,'errorlogin':True})
    else:
        return render(request, 'gestprj/menu.html', {'username': ''})

def logout_view(request):
    logout(request)
    return render(request, 'gestprj/menu.html', {'username': ""})