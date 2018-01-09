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

    #Create account
    url(r'^create_account/', 'principal.views.create_account', name='Registro'),

    #Login
    url(r'^login/', 'principal.views.ingresar', name='Ingresar'),

    #Cerrar sesion
    url(r'^cerrar_sesion/$','principal.views.cerrar_sesion'),
)
