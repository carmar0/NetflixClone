from django.shortcuts import render, redirect

# importamos de forms.py nuestro modelo de formulario personalizado para el registro de nuevos usuarios
from .forms import RegisterForm

# importamos messages del módulo contrib de django para crear mensajes flash(solo duran una actualización de pantalla)
from django.contrib import messages

# importamos las siguientes funcionalidades del módulo autentificador de django
from django.contrib.auth import authenticate, login, logout


# Create your views here.

# vista para la página de inicio
def index(request):

    # renderizamos la plantilla index.html con la variable title en el context data (este context data se usa en
    # la plantilla renderizada)
    return render(request, 'index.html', {
        'title': 'Inicio'
    })


# vista para la página de registro de nuevos usuarios
def register(request):

    # si el usuario ya ha iniciado sesión y está autentificado, se le redirige a la página de Inicio
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        # cargamos el formulario vacío de registro de usuario
        register_form = RegisterForm()

        # si llegan datos del formulario
        if request.method == 'POST':
            # pasamos los datos al modelo de formulario personalizado
            register_form = RegisterForm(request.POST)

            # si el usuario ha rellenado correctamente el formulario, guardamos los datos en la base de datos (se crea
            # una fila en la tabla auth_user) y mostramos por pantalla un mensaje de confirmación de registro
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Te has registrado con éxito. Accede con tu cuenta para ver todo el contenido')
                return redirect('register')

        # renderizamos la plantilla register.html con title y register_form en el context data
        return render(request, 'register.html', {
            'title': 'Completa el formulario',
            'register_form': register_form
        })


# vista para la página de inicio de sesión
def log_in(request):
    # si el usuario ya ha iniciado sesión y quiere iniciarla de nuevo, se redirige a la página Inicio
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        # si llegan datos del formulario de inicio de sesión
        if request.method == 'POST':
            # guardamos el username y password que ha rellenado el usuario
            username = request.POST.get('username')
            password = request.POST.get('password')

            # autentificamos las credenciales del usuario (el método authenticate lo comprueba en la base de datos)
            user = authenticate(request, username=username, password=password)

            # si el usuario es válido, se inicia sesión y se redirige a Inicio. Si no lo es, aparece mensaje de error
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                messages.warning(request, 'El nombre de usuario o la contraseña no son correctos')

        # # renderizamos la plantilla login.html con title en el context data
        return render(request, 'login.html', {
            'title': 'Identifícate'
        })


# vista para la página de cierre de sesión
def log_out(request):
    # cerramos sesión y redirigimos a la página de inicio
    logout(request)
    return redirect('inicio')

# vista para el panel de administración
def admin(request):
    return redirect('admin')
