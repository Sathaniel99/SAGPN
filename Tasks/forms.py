# forms.py
from django import forms
from .models import Ticket, Usuario
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['cliente', 'tecnico', 'situacion', 'area', 'descripcion', 'prioridad', 'realizada']
        labels = {
            'cliente': 'Cliente',
            'tecnico': 'Técnico Asignado (opcional)',
            'situacion': 'Situación',
            'area': 'Área de la Empresa',
            'descripcion': 'Descripción',
            'prioridad': 'Prioridad',
            'realizada': 'Estado de la Tarea',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'tecnico': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'situacion': forms.TextInput(attrs={'class': 'form-control'}),
            'realizada': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role' : 'switch'},),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtener el usuario actual desde kwargs
        super().__init__(*args, **kwargs)

        # Filtra los usuarios excluyendo "Gestor de Tareas" y superusuarios
        self.fields['cliente'].queryset = Usuario.objects.exclude(rol="Gestor de Tareas").exclude(is_superuser=True)
        self.fields['tecnico'].queryset = Usuario.objects.filter(rol="Técnico")

        # Si el usuario es un cliente, establece su ID como valor predeterminado
        if user and user.rol == "Cliente":
            self.initial['cliente'] = user.id

        # Si el usuario es un técnico, establece su ID como valor predeterminado para técnico
        if user and user.rol == "Técnico":
            self.initial['tecnico'] = user.id
            super().__init__(*args, **kwargs)
        
            # Filtra los usuarios excluyendo "Gestor de Tareas" y superusuarios
            self.fields['cliente'].queryset = Usuario.objects.exclude( rol="Gestor de Tareas" ).exclude( is_superuser=True )

class TecnicoForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'rol', 'email']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre/s',
            'last_name': 'Apellido/s',
            'rol': 'Rol',
            'email': 'Correo electrónico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre/s'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido/s'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def __init__(self, *args, **kwargs):
        # Extraer el rol del kwargs (si se pasa desde la vista)
        self.rol = kwargs.pop('rol', 'Técnico')  # Valor predeterminado: "Técnico"
        super().__init__(*args, **kwargs)

        # Establecer el rol inicial
        self.fields['rol'].initial = self.rol

        # Si el rol es fijo (por ejemplo, "Cliente" o "Técnico"), ocultarlo
        if self.rol in ['Cliente', 'Técnico']:
            self.fields['rol'].widget = forms.HiddenInput()

        # Personalizar los widgets de contraseña
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Validar que las contraseñas coincidan
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data