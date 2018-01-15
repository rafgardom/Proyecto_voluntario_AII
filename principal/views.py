# Create your views here.
import util
from django.shortcuts import render_to_response
from models import Deporte, Equipo, Usuario, Noticia
from django.http import HttpResponseRedirect
from django.template import RequestContext
import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import shuffle
from collections import Counter


def main_view(request):
    news_list = Noticia.objects.all().order_by("-moment")[:300]
    news_list = list(news_list.all())
    #shuffle(news_list)

    usuario = None

    try:
        if request.user.is_authenticated():
            usuario = request.user.usuario

        page = request.GET.get('page', 1)

        paginator = Paginator(news_list, 10)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        return render_to_response('home.html', {'request':request, 'news':news, 'usuario':usuario})

    except:
        return render_to_response('home.html', {'request': request, 'usuario': usuario})

@staff_member_required
def populate_teams(request):
    util.populate_equipos_futbol()
    util.populate_equipos_baloncesto()
    util.populate_equipos_f1()
    util.populate_equipos_motogp()
    util.populate_tenis()

    return render_to_response('main.html', {'db_status': "Equipos y deportes generados", 'request':request})

@staff_member_required
def populate_noticias(request):
    
    util.noticias_futbol_as()
    util.noticias_futbol_marca()
    util.noticias_ED()
    util.noticias_f1()
    util.noticias_baloncesto()
    util.noticias_moto()
    util.noticias_tenis_as()
    util.noticias_tenis_marca()
    util.noticias_mgp_as()
    
    return render_to_response('main.html', {'db_status': "Noticias generadas", 'request':request})


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

                        formulario = AuthenticationForm()
                        return render_to_response('login.html',
                                                  {'formulario': formulario, 'bad_login': True, 'request': request}, context_instance=RequestContext(request))
                else:
                    formulario = AuthenticationForm()
                    return render_to_response('login.html', {'formulario':formulario,'bad_login': True, 'request': request}, context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('/')
        else:
            formulario = AuthenticationForm()
        return render_to_response('login.html', {'formulario':formulario, 'user':usuario}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', {'request':request},
                                    context_instance=RequestContext(request))

def create_account(request):
    usuario = request.user.is_authenticated()
    result = None
    try:
        if usuario is not False:
            raise Exception('Accion no permitida')

        if request.method == 'POST':
            formulario = forms.create_user(request.POST)
            if formulario.is_valid():
                try:
                    cd = formulario.cleaned_data
                    if cd.get('password') != cd.get('repeat_password'):
                        raise Exception('Accion no permitida')

                    user = User.objects.create_user(username=cd.get('user_name'),
                                                    email=cd.get('email'),
                                                    password=cd.get('password'))
                    usuario = Usuario.objects.create(user=user, user_name=cd.get('user_name'),
                                                       surname=cd.get('surname'),
                                                       name=cd.get('name'),
                                                       email=cd.get('email'),
                                                       address=cd.get('address'))

                    return render_to_response('home.html', {'good_create': True, 'request': request},context_instance=RequestContext(request))
                except Exception as e:
                    result = render_to_response('create_user.html', {'formulario': formulario, 'request': request, 'bad_login': True},
                                                context_instance=RequestContext(request))
            else:
                result = render_to_response('create_user.html', {'formulario': formulario, 'request': request},
                                            context_instance=RequestContext(request))

        else:
            formulario = forms.create_user()
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

''''@login_required(login_url='/ingresar')
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

    return render_to_response('add_friend.html', {'users': users, 'request': request})'''


@login_required(login_url='/ingresar')
def listing_users_search_box(request):

    if request.method == 'POST':
        formulario = forms.search_user_form(request.POST)
        if formulario.is_valid():
            user = request.user
            usuario = user.usuario
            cd = formulario.cleaned_data
            friends = usuario.friends
            searched_users_list = Usuario.objects.filter(user_name__contains = cd.get('user_name')).exclude(id=usuario.id).exclude(
                id__in=[friend.id for friend in friends.all()])
            new_form = forms.search_user_form()

            friends = usuario.friends
            user_list = Usuario.objects.all().exclude(id=usuario.id).exclude(
                id__in=[friend.id for friend in friends.all()])

            user_list.exclude(id=usuario.id)
            user_list.exclude(id__in=[friend.id for friend in friends.all()])

            page = request.GET.get('page1', 1)
            page2 = request.GET.get('page2', 1)

            paginator = Paginator(user_list, 10)
            paginator2 = Paginator(searched_users_list, 10)
            try:
                users = paginator.page(page)
                searched_users = paginator2.page(page2)
            except PageNotAnInteger:
                users = paginator.page(1)
                searched_users = paginator2.page(5)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
                searched_users = paginator2.page(paginator2.num_pages)

            return render_to_response('add_friend.html', {'request': request,'users': users, 'searched_users': searched_users,
                                                          'formulario':new_form}, context_instance = RequestContext(request))
        else:
            formulario = forms.search_user_form()
            user = request.user
            usuario = user.usuario
            friends = usuario.friends
            user_list = Usuario.objects.all().exclude(id=usuario.id).exclude(
                id__in=[friend.id for friend in friends.all()])
            user_list.exclude(id=usuario.id)
            user_list.exclude(id__in=[friend.id for friend in friends.all()])

            page = request.GET.get('page1', 1)

            paginator = Paginator(user_list, 10)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)

            return render_to_response('add_friend.html',
                                      {'request': request, 'users': users,
                                       'formulario': formulario}, context_instance=RequestContext(request))

    else:
        formulario = forms.search_user_form()

        user = request.user
        usuario = user.usuario
        friends = usuario.friends
        user_list = Usuario.objects.all().exclude(id=usuario.id).exclude(id__in=[friend.id for friend in friends.all()])

        user_list.exclude(id = usuario.id)
        user_list.exclude(id__in=[friend.id for friend in friends.all()])

        page = request.GET.get('page1', 1)

        paginator = Paginator(user_list, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render_to_response('add_friend.html', {'request': request,'users': users,
                                                                  'formulario':formulario}, context_instance = RequestContext(request))
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
def listing_teams_by_country(request, id):
    usuario = request.user.is_authenticated()
    try:
        if usuario is False or request.user.is_staff:
            raise Exception('Accion no permitida')

        sport = Deporte.objects.get(id=id)
        user = request.user
        usuario = user.usuario

        countries = Equipo.objects.values_list('country').filter(sport=sport).exclude(
            id__in=[team.id for team in usuario.favourite_teams.all()])
        countries = list(set(countries))

        return render_to_response('select_sport.html', {'countries': countries, 'request': request, 'sport_id': id})

    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def selected_sport(request,country, id):
    try:
        user = request.user
        usuario = user.usuario
        if usuario is False or request.user.is_staff:
            raise Exception('Accion no permitida')

        sport = Deporte.objects.get(id = id)
        user = request.user
        usuario = user.usuario

        teams_list = sport.equipo_set.exclude(id__in=[team.id for team in usuario.favourite_teams.all()]).filter(country = country)
        countries = Equipo.objects.values_list('country').filter(sport = sport).exclude(id__in=[team.id for team in usuario.favourite_teams.all()])
        countries = list(set(countries))

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


@login_required(login_url='/ingresar')
def my_news(request):
    try:
        user = request.user
        usuario = user.usuario
        if usuario is False or request.user.is_staff:
            raise Exception('Accion no permitida')

        teams = usuario.favourite_teams.all()
        news_list = []
        for team in teams:
            news = Noticia.objects.filter(team = team).order_by('-moment')
            news_list.extend(news)

            news_list = list(set(news_list))

        page = request.GET.get('page', 1)

        paginator = Paginator(news_list, 15)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        return render_to_response('my_news.html', {'request': request, 'news':news, 'usuario':usuario})
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))


def new_view(request, id):
    try:
        if request.user.is_staff:
            raise Exception('Accion no permitida')

        new = Noticia.objects.get(id = id)
        body = str(new.body)
        body = body.split("u'")
        try:
            del body[0]
            del body[-1]
        except:
            pass

        for i in range(len(body)):
            body[i] = body[i][:-3].decode("unicode_escape")

        for i in range(len(body)):
            body[i] = body[i].split(", u")

        body = [item for sublist in body for item in sublist]

        return render_to_response('new_view.html', {'request': request, 'new': new, 'body': body})
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))


'''Recomienda equipos segun los equipos de los amigos del usuario. Si no dispone de amigos, en base a los equipos agregados a favoritos
consultando el deporte y el pais de cada uno de ellos elabora un ranking de equipos afines a sus gustos en base a esos dos parametros.
Se devuelven los 10 equipos mas afines ordenados aleatoriamente. Prioriza los gustos de los amigos con lo que hay mayor probabilidad de
que muestre los equipos favoritos de los amigos que los recomendados por el sistema'''
@login_required(login_url='/ingresar')
def recommended_teams(request):
    user = request.user
    usuario = user.usuario
    has_friends = False

    try:
        if usuario is False or request.user.is_staff:
            raise Exception('Accion no permitida')

        friends_list = usuario.friends.all()
        friend_teams = []
        my_teams = usuario.favourite_teams.all()

        for friend in friends_list:
            friend_teams.extend(friend.favourite_teams.all())

        friend_teams = list(set(friend_teams))

        for team in my_teams:
            if team in friend_teams:
                friend_teams.remove(team)

        if len(friends_list) > 0:
            has_friends = True

        if (len(friends_list) == 0 or len(friend_teams) < 10) and len(my_teams) > 0:
            countries = []
            sport_names = []
            my_teams_names = []
            for team in my_teams:
                countries.append(team.country)
                sport_names.append(team.sport.name)
                my_teams_names.append(team.name)

                sport_names.sort(key=Counter(sport_names).get, reverse=True)
            countries.sort(key=Counter(countries).get, reverse=True)
            countries = list(countries)
            recommended_team_list = []

            if not has_friends:
                del friend_teams[:]

            for sport_name in sport_names:
                team_names_friend_list = [team.name for team in friend_teams]
                sport = Deporte.objects.get(name=sport_name)
                recommended_team_list = Equipo.objects.filter(sport=sport, country=countries[0]).exclude(
                    name__in=my_teams_names).exclude(name__in=team_names_friend_list).all()

                if len(recommended_team_list) == 0:
                    recommended_team_list = Equipo.objects.filter(sport=sport).exclude(
                        name__in=my_teams_names).all()

                recommended_team_list = list(recommended_team_list)
                shuffle(recommended_team_list)

                if len(friend_teams) <= 10 and len(recommended_team_list) >= 5:
                    friend_teams.extend(recommended_team_list[:3])
                    friend_teams = list(set(friend_teams))

                elif len(friend_teams) <= 10:
                    friend_teams.extend(recommended_team_list)
                    friend_teams = list(set(friend_teams))

                if len(friend_teams) == 10:
                    break
            while len(friend_teams) < 10:
                team_names = [team.name for team in friend_teams]
                shuffle(sport_names)
                sport = Deporte.objects.get(name = sport_names[0])
                added_teams = Equipo.objects.filter(sport = sport).exclude(name__in=team_names).exclude(name__in=my_teams_names)
                added_teams = list(added_teams)
                shuffle(added_teams)
                sub_added_teams = added_teams[:1]
                friend_teams.extend(sub_added_teams)

        page = request.GET.get('page', 1)

        if len(friend_teams) >= 10:
            paginator = Paginator(friend_teams[:10], 10)
        else:
            paginator = Paginator(friend_teams, 10)

        try:
            team_list = paginator.page(page)
        except PageNotAnInteger:
            team_list = paginator.page(1)
        except EmptyPage:
            team_list = paginator.page(paginator.num_pages)

        return render_to_response('recommended_teams.html', {'request': request, 'team_list':team_list})
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def add_favourite(request, id):
    try:
        user = request.user
        usuario = user.usuario
        if usuario is False or request.user.is_staff:
            raise Exception('Accion no permitida')

        new = Noticia.objects.get(id=id)

        usuario.favourite_notices.add(new)

        favourite_news = usuario.favourite_notices.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(favourite_news, 15)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        new_list2 = []
        if request.method == 'POST':
            formulario = forms.search_notice_form(request.POST)
            if formulario.is_valid():
                user = request.user
                usuario = user.usuario
                cd = formulario.cleaned_data
                searched_title_new = usuario.favourite_notices.filter(title__contains=cd.get('param')).all()
                searched_body_new = usuario.favourite_notices.filter(body__contains=cd.get('param')).all()

                new_list2.extend(searched_body_new)
                new_list2.extend(searched_title_new)

                new_list2 = list(set(new_list2))

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2,
                                           'formulario': formulario, 'usuario': usuario},
                                  context_instance=RequestContext(request))
            else:

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2,
                                           'formulario': formulario, 'usuario': usuario},
                                  context_instance=RequestContext(request))
        else:
            formulario = forms.search_notice_form()
            return render_to_response('favourite_news.html', {'news': news, 'request': request, 'new_list2': new_list2,
                                                              'formulario': formulario,
                                                              'usuario': usuario, 'new_add_good': True},
                                  context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def erase_favourite(request, id):
    try:
        new = Noticia.objects.get(id = id)
        user = request.user
        usuario = user.usuario
        usuario.favourite_notices.remove(new)

        new_list = usuario.favourite_notices.all()

        page = request.GET.get('page', 1)

        paginator = Paginator(new_list, 10)

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        new_list2 = []
        if request.method == 'POST':
            formulario = forms.search_notice_form(request.POST)
            if formulario.is_valid():
                user = request.user
                usuario = user.usuario
                cd = formulario.cleaned_data
                searched_title_new = usuario.favourite_notices.filter(title__contains = cd.get('param')).all()
                searched_body_new = usuario.favourite_notices.filter(body__contains=cd.get('param')).all()


                new_list2.extend(searched_body_new)
                new_list2.extend(searched_title_new)

                new_list2 = list(set(new_list2))

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2,
                                           'formulario': formulario, 'usuario':usuario},
                                  context_instance=RequestContext(request))
            else:

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2, 'formulario':formulario, 'usuario':usuario},
                                  context_instance=RequestContext(request))
        else:
            formulario = forms.search_notice_form()
            return render_to_response('favourite_news.html', {'news': news, 'request': request, 'new_list2': new_list2, 'formulario':formulario,
                                                              'usuario':usuario, 'new_delete_good': True},
                                  context_instance=RequestContext(request))

    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def favourite_news(request):
    try:

        user = request.user
        usuario = user.usuario

        new_list = usuario.favourite_notices.all()

        page = request.GET.get('page', 1)

        paginator = Paginator(new_list, 10)

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        new_list2 = []
        if request.method == 'POST':
            formulario = forms.search_notice_form(request.POST)
            if formulario.is_valid():
                user = request.user
                usuario = user.usuario
                cd = formulario.cleaned_data
                searched_title_new = usuario.favourite_notices.filter(title__contains = cd.get('param')).all()
                searched_body_new = usuario.favourite_notices.filter(body__contains=cd.get('param')).all()


                new_list2.extend(searched_body_new)
                new_list2.extend(searched_title_new)

                new_list2 = list(set(new_list2))

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2,
                                           'formulario': formulario, 'usuario':usuario},
                                  context_instance=RequestContext(request))
            else:

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2, 'formulario':formulario, 'usuario':usuario},
                                  context_instance=RequestContext(request))
        else:
            formulario = forms.search_notice_form()
            return render_to_response('favourite_news.html', {'news': news, 'request': request, 'new_list2': new_list2, 'formulario':formulario,
                                                              'usuario':usuario},
                                  context_instance=RequestContext(request))

    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def favourite_friend_news(request):
    try:
        user = request.user
        usuario = user.usuario

        new_list = []

        friends = usuario.friends.all()

        for friend in friends:
            new_list.extend(friend.favourite_notices.all())

        page = request.GET.get('page', 1)

        paginator = Paginator(new_list, 10)

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        new_list2 = []
        if request.method == 'POST':
            formulario = forms.search_notice_form(request.POST)
            if formulario.is_valid():
                user = request.user
                usuario = user.usuario
                cd = formulario.cleaned_data
                friends2 = usuario.friends.all()
                new_list2 = []
                for friend in friends2:
                    searched_title_new = friend.favourite_notices.filter(title__contains=cd.get('param')).all()
                    searched_body_new = friend.favourite_notices.filter(body__contains=cd.get('param')).all()
                    new_list2.extend(searched_title_new)
                    new_list2.extend(searched_body_new)

                new_list2 = list(set(new_list2))

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2,
                                           'formulario': formulario, 'usuario': usuario, 'friend_view':True},
                                          context_instance=RequestContext(request))
            else:

                return render_to_response('favourite_news.html',
                                          {'news': news, 'request': request, 'new_list2': new_list2,
                                           'formulario': formulario, 'usuario': usuario, 'friend_view':True},
                                          context_instance=RequestContext(request))
        else:
            formulario = forms.search_notice_form()
            return render_to_response('favourite_news.html', {'news': news, 'request': request, 'new_list2': new_list2,
                                                              'formulario': formulario,
                                                              'usuario': usuario, 'friend_view':True},
                                      context_instance=RequestContext(request))

    except:
        return render_to_response('error.html', {'request': request},
                                  context_instance=RequestContext(request))