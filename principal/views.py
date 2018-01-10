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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main_view(request):
    usuario = request.user.is_authenticated()
    return render_to_response('home.html', {'request':request})

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
        return render_to_response('error.html', {'request':request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def manage_profile(request):
    usuario = request.user.is_authenticated()
    try:
        if usuario is False or request.user.is_staff:
            raise Exception('Accion no permitida')
        user = request.user
        usuario = Usuario.objects.get(user = user)
        teams = usuario.favourite_teams.all()
        friends = usuario.friends.all()

        page1 = request.GET.get('page1', 1)
        page2 = request.GET.get('page2', 1)

        paginator1 = Paginator(friends, 5)
        paginator2 = Paginator(teams, 5)

        try:
            friend_set = paginator1.page(page1)
            teams_set = paginator2.page(page2)
        except PageNotAnInteger:
            friend_set = paginator1.page(1)
            teams_set = paginator2.page(1)
        except EmptyPage:
            friend_set = paginator1.page(paginator1.num_pages)
            teams_set = paginator2.page(paginator2.num_pages)

        return render_to_response('manage_profile.html', {'teams':teams_set, 'friends':friend_set, 'request': request})

    except:
        return render_to_response('error.html', {'request':request},
                                    context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def delete_friend(request, id):
    try:
        friend = Usuario.objects.get(id = id)
        user = request.user
        usuario = user.usuario
        usuario.friends.remove(friend)

        teams = usuario.favourite_teams.all()
        friends = usuario.friends.all()

        page1 = request.GET.get('page1', 1)
        page2 = request.GET.get('page2', 1)

        paginator1 = Paginator(friends, 5)
        paginator2 = Paginator(teams, 5)

        try:
            friend_set = paginator1.page(page1)
            team_set = paginator2.page(page2)
        except PageNotAnInteger:
            friend_set = paginator1.page(1)
            team_set = paginator2.page(1)
        except EmptyPage:
            friend_set = paginator1.page(paginator1.num_pages)
            team_set = paginator2.page(paginator2.num_pages)

        return render_to_response('manage_profile.html', {'teams': team_set, 'friends': friend_set, 'request': request, 'friend_delete_good': True})
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def delete_team(request, id):
    try:
        team = Equipo.objects.get(id = id)
        user = request.user
        usuario = user.usuario
        usuario.favourite_teams.remove(team)

        teams = usuario.favourite_teams.all()
        friends = usuario.friends.all()

        page1 = request.GET.get('page1', 1)
        page2 = request.GET.get('page2', 1)

        paginator1 = Paginator(friends, 5)
        paginator2 = Paginator(teams, 5)

        try:
            friend_set = paginator1.page(page1)
            team_set = paginator2.page(page2)
        except PageNotAnInteger:
            friend_set = paginator1.page(1)
            team_set = paginator2.page(1)
        except EmptyPage:
            friend_set = paginator1.page(paginator1.num_pages)
            team_set = paginator2.page(paginator2.num_pages)

        return render_to_response('manage_profile.html', {'teams': team_set, 'friends': friend_set, 'request': request, 'team_delete_good': True})
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def add_friend(request, id):
    try:
        friend = Usuario.objects.get(id = id)
        user = request.user
        usuario = user.usuario
        usuario.friends.add(friend)

        teams = usuario.favourite_teams.all()
        friends = usuario.friends.all()

        page1 = request.GET.get('page1', 1)
        page2 = request.GET.get('page2', 1)

        paginator1 = Paginator(friends, 5)
        paginator2 = Paginator(teams, 5)

        try:
            friend_set = paginator1.page(page1)
            team_set = paginator2.page(page2)
        except PageNotAnInteger:
            friend_set = paginator1.page(1)
            team_set = paginator2.page(1)
        except EmptyPage:
            friend_set = paginator1.page(paginator1.num_pages)
            team_set = paginator2.page(paginator2.num_pages)

        return render_to_response('manage_profile.html', {'teams': team_set, 'friends': friend_set, 'request': request, 'friend_add_good': True})
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def add_team(request, id):
    try:
        team = Equipo.objects.get(id = id)
        user = request.user
        usuario = user.usuario
        usuario.favourite_teams.add(team)

        teams = usuario.favourite_teams.all()
        friends = usuario.friends.all()

        page1 = request.GET.get('page1', 1)
        page2 = request.GET.get('page2', 1)

        paginator1 = Paginator(friends, 5)
        paginator2 = Paginator(teams, 5)

        try:
            friend_set = paginator1.page(page1)
            team_set = paginator2.page(page2)
        except PageNotAnInteger:
            friend_set = paginator1.page(1)
            team_set = paginator2.page(1)
        except EmptyPage:
            friend_set = paginator1.page(paginator1.num_pages)
            team_set = paginator2.page(paginator2.num_pages)

        return render_to_response('manage_profile.html', {'teams': team_set, 'friends': friend_set, 'request': request, 'team_add_good': True})
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def listing_users(request):

    user = request.user
    usuario = user.usuario
    friends = usuario.friends
    user_list = Usuario.objects.all().exclude(id=usuario.id).exclude(id__in=[friend.id for friend in friends.all()])

    user_list.exclude(id = usuario.id)
    user_list.exclude(id__in=[friend.id for friend in friends.all()])

    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render_to_response('add_friend.html', {'users': users, 'request': request})

@login_required(login_url='/ingresar')
def listing_sports(request):
    usuario = request.user.is_authenticated()
    try:
        if usuario is False or request.user.is_staff:
            raise Exception('Accion no permitida')

        sports = Deporte.objects.all()

        return render_to_response('select_sport.html', {'sports': sports, 'request': request})

    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def selected_sport(request, id):
    try:
        sport = Deporte.objects.get(id = id)
        user = request.user
        usuario = user.usuario

        teams_list = sport.equipo_set.exclude(id__in=[team.id for team in usuario.favourite_teams.all()])
        page = request.GET.get('page', 1)

        paginator = Paginator(teams_list, 10)
        try:
            teams = paginator.page(page)
        except PageNotAnInteger:
            teams = paginator.page(1)
        except EmptyPage:
            teams = paginator.page(paginator.num_pages)

        return render_to_response('add_team.html', {'teams': teams, 'request': request})

    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def listing_teams(request):

    user = request.user
    usuario = user.usuario
    football = Deporte.objects.get(name = "Futbol")
    tennis = Deporte.objects.get(name="Tenis")
    motogp = Deporte.objects.get(name="Moto GP")
    formula_one = Deporte.objects.get(name="Formula 1")
    basket = Deporte.objects.get(name="Baloncesto")

    football_teams = football.equipo_set.exclude(id__in=[team.id for team in usuario.favourite_teams.all()])
    tennis_teams = tennis.equipo_set.exclude(id__in=[team.id for team in usuario.favourite_teams.all()])
    motogp_teams = motogp.equipo_set.exclude(id__in=[team.id for team in usuario.favourite_teams.all()])
    f1_teams = formula_one.equipo_set.exclude(id__in=[team.id for team in usuario.favourite_teams.all()])
    basket_teams = basket.equipo_set.exclude(id__in=[team.id for team in usuario.favourite_teams.all()])

    football_page = request.GET.get('page', 1)
    tennis_page = request.GET.get('page', 1)
    motogp_page = request.GET.get('page', 1)
    f1_page = request.GET.get('page', 1)
    basket_page = request.GET.get('page', 1)


    football_paginator = Paginator(football_teams, 10)
    tennis_paginator = Paginator(tennis_teams, 10)
    motogp_paginator = Paginator(motogp_teams, 10)
    f1_paginator = Paginator(f1_teams, 10)
    basket_paginator = Paginator(basket_teams, 10)
    try:
        footballs = football_paginator.page(football_page)
        tennises = tennis_paginator.page(tennis_page)
        motogps = motogp_paginator.page(motogp_page)
        fones = f1_paginator.page(f1_page)
        baskets = basket_paginator.page(basket_page)
    except PageNotAnInteger:
        footballs = football_paginator.page(1)
        tennises = tennis_paginator.page(1)
        motogps = motogp_paginator.page(1)
        fones = f1_paginator.page(1)
        baskets = basket_paginator.page(1)
    except EmptyPage:
        footballs = football_paginator.page(football_paginator.num_pages)
        tennises = tennis_paginator.page(tennis_paginator.num_pages)
        motogps = motogp_paginator.page(motogp_paginator.num_pages)
        fones = f1_paginator.page(f1_paginator.num_pages)
        baskets = basket_paginator.page(basket_paginator.num_pages)

    return render_to_response('add_team.html', {'footballs': footballs, 'tennises': tennises, 'motogps': motogps,
                                                'fones': fones, 'baskets': baskets, 'request': request})