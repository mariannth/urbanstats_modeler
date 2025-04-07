from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, MensajeContacto

# class RegistroForm(UserCreationForm):
#     class Meta:
#         model = Usuario
#         fields = ('username', 'email')
#         labels = {
#             'username': 'Nombre de usuario',
#             'email': 'Correo electrónico',
#         }

class RegistroForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ["username", "email", "password1", "password2"]


class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']