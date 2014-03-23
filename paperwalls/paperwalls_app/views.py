from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from datetime import datetime


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
            obj = album.save(commit=False)
            obj.creador = request.user
            obj.save()
            return HttpResponseRedirect('/')
    return render_to_response('Albumes/alta_album.html', 
        {'album': album}, 
        context_instance=RequestContext(request))


def modificar_album(request):
    buscador = BuscadorAlbumForm()
    formulario = ''
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

    return render_to_response('Albumes/modificar_album.html',{'album': formulario,'buscar':buscador},context_instance=RequestContext(request)) 
    
def baja_album(request):
    if request.method=='POST':
        album = str(request.REQUEST["album_1"])
        album = get_object_or_404(Album, pk = album)
        formulario = AlbumForm(request.POST, instance=album)
        if formulario.is_valid():
            nombre_album = album.titulo
            if request.REQUEST["input-confirma-borrar"]== 'true':
                album.delete()
                print 'El album %s ha sido borrado junto con sus imagenes!'%(nombre_album) # a futuro quitar los prints y utilizar mensajes en los templates para mejor feedback
            return HttpResponseRedirect('/') 
    else:
        if "album_1" in request.REQUEST:
            album = str(request.REQUEST["album_1"])
            album = get_object_or_404(Album, pk = album)
            buscador = BuscadorAlbumForm(request.REQUEST)
            formulario = AlbumForm(instance = album)
        else:
            buscador = BuscadorAlbumForm()
            formulario = ""
    return render_to_response('Albumes/baja_album.html', {'album': formulario, 'buscar':buscador}, context_instance=RequestContext(request))





def alta_imagen(request):
    if request.method == "GET":        
        imagen = ImagenForm()
    else:
        imagen = ImagenForm(request.POST, request.FILES)
        if imagen.is_valid():
            obj = imagen.save(commit=False)
            obj.user = request.user
            obj.save()
            imagen.save_m2m()
            return HttpResponseRedirect('/')
    return render_to_response('Imagen/alta_imagen.html', 
        {'imagen': imagen},context_instance=RequestContext(request))                    

def modificar_imagen(request):
    buscador = BuscadorImagenForm()
    formulario = ''
    preview = ''
    if request.method=='POST':
        imagen = int(request.REQUEST["imagen_1"])
        imagen = get_object_or_404(Imagen, pk = imagen)
        formulario = ImagenForm(request.POST, instance=imagen)
        print formulario.is_valid()
        if formulario.is_valid():
            formulario.save()
            print 'imagen data modified successfully!'
            return HttpResponseRedirect('/')
    else:
        if "imagen_1" in request.REQUEST:
            imagen = int(request.REQUEST["imagen_1"])
            imagen = get_object_or_404(Imagen, pk = imagen)
            buscador = BuscadorImagenForm(request.REQUEST)
            formulario = ImagenForm(instance = imagen)
            preview = imagen.imagen.url
    return render_to_response('Imagen/modificar_imagen.html',{'imagen': formulario,'buscar':buscador,'preview':preview},context_instance=RequestContext(request)) 

def baja_imagen(request):
    preview = ''
    if request.method=='POST':
        imagen = str(request.REQUEST["imagen_1"])
        imagen = get_object_or_404(Imagen, pk = imagen)
        formulario = ImagenForm(request.POST, instance=imagen)
        if formulario.is_valid():
            imagen.delete()    
            return HttpResponseRedirect('/') 
    else:
        if "imagen_1" in request.REQUEST:
            imagen = str(request.REQUEST["imagen_1"])
            imagen = get_object_or_404(Imagen, pk = imagen)
            buscador = BuscadorImagenForm(request.REQUEST)
            formulario = ImagenForm(instance = imagen)
            preview = imagen.imagen.url
        else:
            buscador = BuscadorImagenForm()
            formulario = ""
    return render_to_response('Imagen/baja_imagen.html', {'imagen': formulario, 'buscar':buscador,'preview':preview}, context_instance=RequestContext(request))






#ABM Categorias - Funcionando --> TODO:  integrar mensajes para mejor feedback
def alta_categoria(request):
    if request.method == "GET":
        categoria = CategoriaForm() 
    else:
        categoria = CategoriaForm(request.POST)
        if categoria.is_valid():
            categoria.save()
            return HttpResponseRedirect('/')
    return render_to_response('Categorias/alta_categoria.html', 
        {'categoria': categoria}, 
        context_instance=RequestContext(request))

def modificar_categoria(request):
    buscador = BuscadorCategoriaForm()
    formulario = ''
    if request.method=='POST':
        categoria = int(request.REQUEST["categoria_1"])
        categoria = get_object_or_404(Categoria, pk = categoria)
        formulario = CategoriaForm(request.POST, instance=categoria)
        print formulario.is_valid()
        if formulario.is_valid():
            formulario.save()
           
            return HttpResponseRedirect('/')
    else:
        if "categoria_1" in request.REQUEST:
            categoria = int(request.REQUEST["categoria_1"])
            categoria = get_object_or_404(Categoria, pk = categoria)
            buscador = BuscadorCategoriaForm(request.REQUEST)
            formulario = CategoriaForm(instance = categoria)
            
    return render_to_response('Categorias/modificar_categoria.html',{'categoria': formulario,'buscar':buscador},context_instance=RequestContext(request)) 

def baja_categoria(request):
    if request.method=='POST':
        categoria = str(request.REQUEST["categoria_1"])
        categoria = get_object_or_404(Categoria, pk = categoria)
        formulario = CategoriaForm(request.POST, instance=categoria)
        if formulario.is_valid():
            nombre_categoria = categoria.nombre
            if categoria.imagen_set.count() == 0 :
                categoria.delete()
                print 'La categoria %s ha sido borrada!'%(nombre_categoria) # a futuro quitar los prints y utilizar mensajes en los templates para mejor feedback
            else:
                print 'La categoria %s no puede ser eliminada debido a que hay imagenes relacionadas'%(nombre_categoria)
            return HttpResponseRedirect('/') 
    else:
        if "categoria_1" in request.REQUEST:
            categoria = str(request.REQUEST["categoria_1"])
            categoria = get_object_or_404(Categoria, pk = categoria)
            buscador = BuscadorCategoriaForm(request.REQUEST)
            formulario = CategoriaForm(instance = categoria)
        else:
            buscador = BuscadorCategoriaForm()
            formulario = ""
    return render_to_response('Categorias/baja_categoria.html', {'categoria': formulario, 'buscar':buscador}, context_instance=RequestContext(request))







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
            return HttpResponseRedirect('ingresar')
    else:
        formulario = UserCreationForm(instance = get_object_or_404(User, username='jjose') )
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