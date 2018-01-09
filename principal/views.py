# Create your views here.
import util
from django.shortcuts import render_to_response
from models import Deporte, Equipo, Usuario
from django.http import HttpResponseRedirect
from django.template import RequestContext
import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def main_view(request):
    usuario = request.user.is_authenticated()
    return render_to_response('main.html', {'request':request})

@staff_member_required
def populate_teams(request):
    usuario = request.user.is_authenticated()
    Deporte.objects.all().delete()

    util.populate_equipos_futbol()
    util.populate_equipos_baloncesto()
    util.populate_equipos_f1()
    util.populate_equipos_motogp()
    util.populate_tenis()

    return render_to_response('main.html', {'db_status': "Equipos y deportes generados", 'request':request})

@login_required(login_url='/ingresar')
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')

def ingresar(request):
    usuario = request.user.is_authenticated()
    try:
        if usuario is not False:
            raise Exception('Accion no permitida')

        if request.method == 'POST':
            formulario = AuthenticationForm(request.POST)
            if formulario.is_valid:
                usuario = request.POST['username']
                clave = request.POST['password']
                acceso = authenticate(username = usuario, password = clave)
                if acceso is not None:
                    if acceso.is_active:
                        login(request, acceso)
                        return HttpResponseRedirect('/')
                    else:
                        return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else:
            formulario = AuthenticationForm()
        return render_to_response('login.html', {'formulario':formulario, 'user':usuario}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', {'user':usuario},
                                    context_instance=RequestContext(request))

def create_account(request):
    usuario = request.user.is_authenticated()
    fail = False

    try:
        if usuario is not False:
            raise Exception('Accion no permitida')

        if request.method == 'POST':
            formulario = forms.create_user(request.POST)
            if formulario.is_valid():
                try:
                    cd = formulario.cleaned_data
                    user = User.objects.create_user(username=cd.get('user_name'),
                                                    email=cd.get('email'),
                                                    password=cd.get('password'))
                    usuario = Usuario.objects.create(user=user, user_name=cd.get('user_name'),
                                                       surname=cd.get('surname'),
                                                       name=cd.get('name'),
                                                       email=cd.get('email'),
                                                       address=cd.get('address'))
                    return HttpResponseRedirect('/')
                except Exception as e:
                    fail = True
                    result = render_to_response('error.html',
                                                context_instance=RequestContext(request))

        else:
            formulario = forms.create_user()

        if fail == False:
            result = render_to_response('create_user.html', {'formulario': formulario, 'request':request},
                                        context_instance=RequestContext(request))
        return result

    except:
        return render_to_response('error.html',
                                  context_instance=RequestContext(request))

def manage_profile(request):
    usuario = request.user.is_authenticated()
    #try:
    '''if usuario is not False or request.user.is_staff:
        raise Exception('Accion no permitida')'''
    user = request.user
    usuario = Usuario.objects.get(user = user)
    teams = usuario.favourite_teams
    friends = usuario.friends

    #TODO voy por el la gestion del perfil. Primero muestro el perfil ya definido en plan los equipos favoritos y sus amigos. Lo proximo es en este mismo metodo poner el aniadir amigos/equipos favoritos

    #TODO Gestion de amigos: comprobar que el usuario en cuestion no se aniade a amigo a si mismo
    return render_to_response('manage_profile.html', {'teams':teams, 'friends':friends, 'request': request})

    '''except:
        return render_to_response('error.html', {'user':usuario},
                                    context_instance=RequestContext(request))'''

