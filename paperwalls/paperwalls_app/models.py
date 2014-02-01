#! /usr/bin/python2
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from string import join
import os
from PIL import Image as PImage
from paperwalls.settings import MEDIA_ROOT
from thumbs import ImageWithThumbsField #crea automaticamente thumbnails para cada img subida




class Etiqueta(models.Model):
    etiqueta = models.CharField(max_length=50)
    def __unicode__(self):
        return self.etiqueta

class Imagen(models.Model):
    imagen = ImageWithThumbsField(upload_to="images/", sizes=((40,40),(128,128)))
    etiquetas = models.ManyToManyField(Etiqueta)
    album = models.ForeignKey("Album")
    creacion = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True)
    categoria = models.ForeignKey("Categoria")

    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Imagen, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.imagen.name))
        self.width, self.height = im.size
        super(Imagen, self).save(*args, ** kwargs)

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
    
    def imagenes(self):
        lst = [x.imagen.name for x in self.imagen_set.all()]
        lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return join(lst, ', ')
    imagenes.allow_tags = True

    def __unicode__(self):
        return self.titulo


        