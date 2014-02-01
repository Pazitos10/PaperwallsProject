from paperwalls_app.models import *
from django.contrib import admin
from django.utils.safestring import mark_safe

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["titulo"]
    list_display = ["titulo","imagenes"]

class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ["etiqueta"]

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]    

class ImagenAdmin(admin.ModelAdmin):
    list_display = ["thumb_img", "user", "tags", "creacion","tamanio","categoria","__unicode__"]
    list_filter = ["etiquetas", "user"]

    def thumb_img(self, obj):
        if obj.imagen:
            print obj.imagen
            return  mark_safe("""<a href="%s" ><img border="0" alt="" src="%s" /></a>""") % (
                        obj.imagen.url , obj.imagen.url_40x40)
        else:
            return '(Sin imagen)'
    thumb_img.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(Album, AlbumAdmin)
admin.site.register(Etiqueta, EtiquetaAdmin)
admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Categoria, CategoriaAdmin)