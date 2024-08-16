from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Tema, Comentario
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nombre', 'descripcion']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'archivo']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresá una dirección de email válida.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El email ya está en uso. Por favor, elegí uno diferente.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden")
            try:
                validate_password(password1, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)
        
        return password2

class ActualizarPerfilForm(forms.ModelForm):
    foto_perfil = forms.ImageField(required=False, help_text="Sube una imagen de perfil (opcional).")

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'foto_perfil']  # Incluye el campo para la foto de perfil

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("El email ya está en uso. Por favor, elegí uno diferente.")
        return email
