# Uncomment the next two lines to enable the admin:
from django.conf.urls import patterns, include, url
from django.contrib import admin

import paperwalls_app
from paperwalls_app.views import *
 

admin.autodiscover()

from django.conf import settings

# ... the rest of your URLconf goes here ...



urlpatterns = patterns('',
    # Examples:




    url(r'^$', 'paperwalls_app.views.main', name='main'),

    # Gestion de Albumes
    url(r'^albumes/alta$', 'paperwalls_app.views.alta_album', name='alta_album'),
    url(r'^albumes/modificar$', 'paperwalls_app.views.modificar_album', name='modificar_album'),
    url(r'^albumes/baja$', 'paperwalls_app.views.baja_album', name='baja_album'),

    # Gestion de Imagenes
    url(r'^albumes/imagen/alta$', 'paperwalls_app.views.alta_imagen', name='alta_imagen'),
    url(r'^albumes/imagen/modificar$', 'paperwalls_app.views.modificar_imagen', name='modificar_imagen'),
    url(r'^albumes/imagen/baja$', 'paperwalls_app.views.baja_imagen', name='baja_imagen'),
    url(r'^imagen/(?P<id_imagen>\d+)$', 'paperwalls_app.views.view_image', name='view_image'),
    url(r'^imagen/(?P<filename>.*)$', 'paperwalls_app.views.file_download',name='file_download'),


    # Gestion de Categorias
    url(r'^albumes/categoria/alta$', 'paperwalls_app.views.alta_categoria', name='alta_categoria'),
    url(r'^albumes/categoria/modificar$', 'paperwalls_app.views.modificar_categoria', name='modificar_categoria'),
    url(r'^albumes/categoria/baja$', 'paperwalls_app.views.baja_categoria', name='baja_categoria'),


    # url(r'^paperwalls/', include('paperwalls.foo.urls')),

    # URLs usuarios
    url(r'^usuarios/registrar$', 'paperwalls_app.views.nuevo_usuario', name='nuevo_usuario'),
    url(r'^usuarios/ingresar$', 'paperwalls_app.views.ingresar', name='ingresar'),
    url(r'^paperwalls$', 'paperwalls_app.views.home', name='home'),
    url(r'^paperwalls/logout$', 'paperwalls_app.views.salir', name='salir'),


   
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^selectable/', include('selectable.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
else:
    handler404 = 'paperwalls_app.views.paperwalls_app_404_error'
    handler500 = 'paperwalls_app.views.paperwalls_app_500_error'

