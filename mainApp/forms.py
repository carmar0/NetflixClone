from django import forms
# Del módulo de autentificación de usuarios de django, importamos UserCreationForm (para crear
# un nuevo usuario a través de un formulario predefinido) y el modelo User.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# modelo de formulario para el registro de un nuevo usuario en la web
class RegisterForm(UserCreationForm):

    # Se tiene que introducir obligatoriamente un email para poder registrarse
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # campos del formulario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


