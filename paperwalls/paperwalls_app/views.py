from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext


#Manejo de usuarios
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
#Manejo de usuarios 

#Descarga de imagenes
from django.core.servers.basehttp import FileWrapper
import mimetypes
import os
#Descarga de imagenes

from paperwalls.settings import MEDIA_URL,MEDIA_ROOT
from paperwalls_app.models import *
from paperwalls_app.forms import * 






def main(request):
    """Main listing."""
    albums = Album.objects.all()
    imagenes = Imagen.objects.all()

    paginator = Paginator(albums, 5)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        albums = paginator.page(page)
    except (InvalidPage, EmptyPage):
        albums = paginator.page(paginator.num_pages)

    for album in albums.object_list:
        album.imagenes = album.imagenes()[:4]
   
    return render_to_response("list-recent.html", dict(albums=albums, imagenes=imagenes, user=request.user,
        media_url=MEDIA_URL))


def alta_album(request):
    if request.method == "GET":
        album = AlbumForm() 
    else:
        album = AlbumForm(request.POST)
        if album.is_valid():
            album.save()
            return HttpResponseRedirect('/')
    return render_to_response('Albumes/alta_album.html', 
        {'album': album}, 
        context_instance=RequestContext(request))

#Terminar
def modificar_album(request):
    pass
    '''
    buscador = BuscadorAlbumForm()
    album = ''
    if request.method=='POST':
        album = int(request.REQUEST["album_1"])
        album = get_object_or_404(Album, pk = album)
        formulario = AlbumForm(request.POST, instance=album)
        if formulario.is_valid():
            formulario.save()
            print 'album data modified successfully!'
            return HttpResponseRedirect('/')
    else:
        if "album_1" in request.REQUEST:
            album = int(request.REQUEST["album_1"])
            album = get_object_or_404(Album, pk = album)
            buscador = BuscadorAlbumForm(request.REQUEST)
            formulario = AlbumForm(instance = album)
    return render_to_response('Albumes/modificar_album.html',{'album': album,'buscar':buscador},context_instance=RequestContext(request)) 
    '''        
    
def baja_album(request):
    pass


def alta_imagen(request):
    if request.method == "GET":        
        imagen = ImagenForm()
    else:
        imagen = ImagenForm(request.POST, request.FILES)
        if imagen.is_valid():
            imagen.save()
            etiquetas = imagen.cleaned_data['Tags']      #obtenemos etiquetas desde el campo customizado
            tags = etiquetas.split(', ')            #separamos las mismas y las almacenamos en una lista
            for tag in tags:                        #por cada palabra creamos una etiqueta y la guardamos en la base
                e = Etiqueta()
                e.etiqueta = tag
                e.save()
                imagen.instance.etiquetas.add(e) 
            return HttpResponseRedirect('/')
    return render_to_response('Imagen/alta_imagen.html', 
        {'imagen': imagen},context_instance=RequestContext(request))                    

def modificar_imagen(request):
    pass

def baja_imagen(request):
    pass




def alta_categoria(request):
    if request.method == "GET":
        categoria = CategoriaForm() 
    else:
        categoria = CategoriaForm(request.POST)
        if categoria.is_valid():
            categoria.save()
            return HttpResponseRedirect('/')
        else:
            print categoria.errors
    return render_to_response('Categorias/alta_categoria.html', 
        {'categoria': categoria}, 
        context_instance=RequestContext(request))

def modificar_categoria(request):
    pass

def baja_categoria(request):
    pass

def view_image(request, id_imagen):
    i = get_object_or_404(Imagen, pk = id_imagen)
    return render_to_response('Otro/view-image.html',{'imagen':i.imagen,'obj':i},context_instance=RequestContext(request))

def galeria(request):
    return render_to_response('Otro/galeria.html',context_instance=RequestContext(request))



#Vistas para manejo usuarios

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('usuarios/ingresar')
    else:
        formulario = UserCreationForm()
    return render_to_response('usuarios/nuevousuario.html',{'formulario':formulario},context_instance=RequestContext(request))

def ingresar(request):
    if request.method == "POST":
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            usuario = request.POST['username']
            password = request.POST['password']
            acceso = authenticate(username=usuario,password=password)
            if acceso is not None and acceso.is_active:
                login(request,acceso)
                return HttpResponseRedirect('/paperwalls') #debe ir a home-> otra vista con opciones diferentes
    else:
        formulario = AuthenticationForm()
    return render_to_response('usuarios/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url = 'usuarios/ingresar')
def salir(request):
    logout(request)
    return HttpResponseRedirect('/') #Debe ir al template que ven todos cuando accedan a paperwalls por primera vez


@login_required(login_url = 'usuarios/ingresar')
def home(request):
    usuario = request.user
    return render_to_response('Otro/home.html',{'usuario':usuario},context_instance=RequestContext(request))



#Administracion de errores -> Falta probar
def paperwalls_app_404_error(request):
    return render_to_response('Otro/404.html',context_instance=RequestContext(request))

def paperwalls_app_500_error(request):
    return render_to_response('Otro/500.html',context_instance=RequestContext(request))



#Descarga de imagenes Funciona

def file_download(request, filename):
    filepath = os.path.join(MEDIA_ROOT, filename)    
    wrapper = FileWrapper(open(filepath, 'rb'))
    content_type = mimetypes.guess_type(filepath)[0]
    response = HttpResponse(wrapper, mimetype=content_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response