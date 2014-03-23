#! /usr/bin/python2
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from string import join
import os
from PIL import Image as PImage
from paperwalls.settings import MEDIA_ROOT
from thumbs import ImageWithThumbsField #crea automaticamente thumbnails para cada img subida

from taggit.managers import TaggableManager


class Imagen(models.Model):
    imagen = ImageWithThumbsField(upload_to="images/", sizes=((40,40),(128,128)))
    etiquetas = TaggableManager()
    album = models.ForeignKey("Album",null=False,blank=False)
    creacion = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User)
    categoria = models.ForeignKey("Categoria",null=False,blank=False)
    publica = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Imagen, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.imagen.name))
        self.width, self.height = im.size
        super(Imagen, self).save(*args, ** kwargs)
    
    def delete(self, *args, **kwargs):
        for tag in self.etiquetas.all():
            tag.delete()
        self.imagen.delete() #se supone que borra la imagen fisica y sus thumbnails pero tira error
        super(Imagen, self).delete(*args, **kwargs)
    


    def __unicode__(self):
        return self.imagen.name
    
    def tamanio(self):
        return "%s x %s" % (self.width, self.height)

    def tags(self):
        lst = [x[1] for x in self.etiquetas.values_list()]
        return str(join(lst, ', '))


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)


    def __unicode__(self):
        return self.nombre

class Album(models.Model):
    titulo = models.CharField(max_length=60, unique=True)
    creador = models.ForeignKey(User)

    def imagenes(self):
        lst = [x.imagen.name for x in self.imagen_set.all()]
        lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return join(lst, ', ')
    imagenes.allow_tags = True

    def __unicode__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        for img in self.imagen_set.all():
            img.delete()
        super(Album, self).delete(*args, **kwargs)
    

        