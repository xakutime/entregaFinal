from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='pagina_inicio'),
    path('tema/<int:tema_id>/', views.tema_detalle, name='tema_detalle'),
    path('crear_tema/', views.crear_tema, name='crear_tema'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    path('perfil/', views.actualizar_perfil, name='perfil'),
    path('about/', views.about, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)