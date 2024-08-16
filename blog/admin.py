from django.contrib import admin
from .models import Tema, Comentario

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('tema', 'autor', 'texto', 'fecha')
    list_filter = ('tema', 'autor')