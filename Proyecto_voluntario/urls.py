from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Proyecto_voluntario.views.home', name='home'),
    # url(r'^Proyecto_voluntario/', include('Proyecto_voluntario.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #home
    url(r'^$', 'principal.views.main_view', name='Inicio'),

    #populate
    url(r'^populateTeams/', 'principal.views.populate_teams', name='Populate equipos'),
    url(r'^populateNoticias/', 'principal.views.populate_noticias', name='Populate noticias'),

    #Create account
    url(r'^create_account/', 'principal.views.create_account', name='Registro'),

    #Login
    url(r'^login/', 'principal.views.ingresar', name='Ingresar'),

    #Cerrar sesion
    url(r'^cerrar_sesion/$','principal.views.cerrar_sesion'),

    #Manage profile
    url(r'^profile/$','principal.views.manage_profile'),

    #Delete friend
    url(r'^delete_friend/(?P<id>\d+)/$', 'principal.views.delete_friend', name="delete_friend"),

    #Delete team
    url(r'^delete_team/(?P<id>\d+)/$', 'principal.views.delete_team', name="delete_team"),

    #List users
    url(r'^list_users/$','principal.views.listing_users_search_box'),

    #List teams
    url(r'^list_teams/$','principal.views.listing_teams'),

    #Select sports
    url(r'^select_sports/$','principal.views.listing_sports'),

    #Select sport
    url(r'^selected_sport/(?P<id>\d+)/$', 'principal.views.listing_teams_by_country', name="selected_sport"),

    #Select sport by country1
    url(r'^selected_sport_country/(?P<country>\w+?\W+?\w+?\W+)(?P<id>\d+)/$', 'principal.views.selected_sport', name="selected_sport_country1"),

    #Select sport by country2
    url(r'^selected_sport_country/(?P<country>\W+\w+\W+)(?P<id>\d+)/$', 'principal.views.selected_sport', name="selected_sport_country2"),

    #Select sport by country3
    url(r'^selected_sport_country/(?P<country>\w+\W+\w+)(?P<id>\d+)/$', 'principal.views.selected_sport', name="selected_sport_country3"),

    #Select sport by country4
    url(r'^selected_sport_country/(?P<country>\w+)(?P<id>\d+)/$', 'principal.views.selected_sport', name="selected_sport_country4"),

    #Add friend
    url(r'^add_friend/(?P<id>\d+)/$', 'principal.views.add_friend', name="add_friend"),

    #Add team
    url(r'^add_team/(?P<id>\d+)/$', 'principal.views.add_team', name="add_team"),

    #My news
    url(r'^my_news/$', 'principal.views.my_news', name="my_news"),

    #Watch new
    url(r'^watch_new/(?P<id>\d+)/$', 'principal.views.new_view', name="watch_new"),
)
