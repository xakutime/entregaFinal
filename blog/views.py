from django.shortcuts import render, redirect, get_object_or_404
from .models import Tema, Comentario, Perfil
from .forms import TemaForm, ComentarioForm, RegistroUsuarioForm, ActualizarPerfilForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

def inicio(request):
    temas = Tema.objects.all()
    return render(request, 'blog/inicio.html', {'temas': temas})

def tema_detalle(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    comentarios = Comentario.objects.filter(tema=tema)
    mensaje_error = None
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            mensaje_error = "Debes tener un usuario para agregar un comentario."
            form = ComentarioForm(request.POST, request.FILES)
            # No procesamos el formulario si el usuario no está autenticado
        else:
            form = ComentarioForm(request.POST, request.FILES)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.tema = tema
                comentario.autor = request.user
                comentario.save()
                return redirect('tema_detalle', tema_id=tema_id)
    else:
        form = ComentarioForm()
    
    return render(request, 'blog/tema_detalle.html', {
        'tema': tema,
        'comentarios': comentarios,
        'form': form,
        'mensaje_error': mensaje_error
    })

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.email = form.cleaned_data.get('email')
            usuario.save()
            print(f"Usuario {usuario.username} creado correctamente con email {usuario.email}")
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('pagina_inicio')
            else:
                # Si el formulario no es válido, los errores se mostrarán en la plantilla
                form.add_error(None, "Hubo un problema al autenticar el usuario.")
        else:
            print(form.errors)
    else:
        form = RegistroUsuarioForm()
    return render(request, 'blog/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')  # Redirigir al perfil después del login
        else:
            return render(request, 'blog/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'blog/login.html', {'error': None})

@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        form = ActualizarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Actualizar el perfil asociado con el usuario, si existe
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            if 'foto_perfil' in request.FILES:
                perfil.foto_perfil = request.FILES['foto_perfil']
            perfil.nombre = form.cleaned_data.get('first_name')
            perfil.apellido = form.cleaned_data.get('last_name')
            perfil.save()
            return redirect('pagina_inicio')
    else:
        form = ActualizarPerfilForm(instance=request.user)
    
    return render(request, 'blog/actualizar_perfil.html', {'form': form})


@login_required
def crear_tema(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para crear temas.")
    
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_inicio')
    else:
        form = TemaForm()
    
    return render(request, 'blog/crear_tema.html', {'form': form})

def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    if not request.user.is_superuser and comentario.autor != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")
    
    if request.method == 'POST':
        comentario.delete()
        return redirect('tema_detalle', tema_id=comentario.tema.id)

    return render(request, 'blog/eliminar_confirmacion.html', {'comentario': comentario})

def about(request):
    return render(request, 'blog/about.html')

def logout_view(request):
    logout(request)
    return redirect('pagina_inicio')
