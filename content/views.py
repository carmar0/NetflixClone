from django.shortcuts import render, redirect
from .models import Film, Series, Customed

# importamos messages del módulo contrib de django para crear mensajes flash(solo duran un refresh de pantalla)
from django.contrib import messages

# para la barra de búsqueda
from django.db.models import Q

# Importamos el decorador login_required para restringir el acceso a ciertas páginas de la web si no se ha iniciado
# sesión. Los decoradores son funcionalidades que se ejecutan previamente a la funcionalidad de una vista
from django.contrib.auth.decorators import login_required

# para realizar los gráficos de estadísticas de usuario
from .graph import get_hbar_graph, get_hbar_graph2
from django.contrib.auth.models import User

# Create your views here.

# vista para la página de películas
@login_required(login_url="login")  # el usuario debe haber iniciado sesión para ver la página de Películas
def films(request):

    # búsqueda que ha escrito el usuario
    search = request.GET.get("buscar")

    # consultamos en la base de datos las películas que hay
    films = Film.objects.all()

    # si el usuario está buscando algo
    if search:
        films = Film.objects.filter(
            Q(title__icontains = search) | Q(genre__icontains = search)
              # icontains (no importa que se escriba incompletamente el título o género en la búsqueda)
        )

    # renderizamos films.html con title, films y search en el context data
    return render(request, 'films.html', {
        'title': 'Películas',
        'films': films,
        'search': search
    })

# vista para la página individual de cada película
@login_required(login_url="login")
def film_page(request, film_title, previous_url): # los parámetro film_title y previous_url llegan a través de la URL

    # al cargarse la vista por primera vez, guardamos la url de la que venimos (la usamos para el botón Volver)
    if previous_url == 'back_to_films':
        back_url = 'http://127.0.0.1:8000/peliculas/'
    elif previous_url == 'back_to_series':
        back_url = 'http://127.0.0.1:8000/series/'
    elif previous_url == 'back_to_favorites':
        back_url = 'http://127.0.0.1:8000/favoritos/'
    elif previous_url == 'back_to_seeAgain':
        back_url = 'http://127.0.0.1:8000/volver-a-ver/'

    # obtenemos la instancia de la película en cuestión
    film = Film.objects.get(title=film_title)

    # obtenemos la instancia de contenido por usuario para saber si ya la ha marcado como visto o guardado en favoritos
    customed= Customed.objects.filter(title=film.title, user_id=request.user.id)  # title=film_title=film.title

    # si llegan datos del formulario (marcado como visto y/o guardado en favoritos)
    if request.method == 'POST':

        # si aún no existe un registro tipo Customed para esta película y usuario
        if not customed:

            # Comprobación de que se ha rellenado correctamente el formulario
            if request.POST.get("seen_check") and request.POST.get("notSeen_check") or request.POST.get(
                    "favorite_check") and request.POST.get("notFavorite_check") or request.POST.get(
                "notSeen_check") or request.POST.get("notFavorite_check"):
                messages.warning(request, 'Opción no válida. Selecciona máximo dos opciones')
                return redirect('film_page', film_title, previous_url)

            # si el usuario ha seleccionado los check de Visto y Guardar en Favoritos
            if request.POST.get("seen_check") and request.POST.get("favorite_check"):
                # creamos el nuevo registro y lo guardamos en la base de datos
                customed_register = Customed(title=film.title, description=film.description, time=film.time,
                                             genre=film.genre, image=film.image, release_date=film.release_date,
                                             user_id=request.user.id, category="Película", seen=True, favorite=True)
                customed_register.save()

            # si el usuario solo ha seleccionado el check de Visto
            elif request.POST.get("seen_check"):
                customed_register = Customed(title=film.title, description=film.description, time=film.time,
                                             genre=film.genre, image=film.image, release_date=film.release_date,
                                             user_id=request.user.id, category="Película", seen=True)
                customed_register.save()

            # si el usuario solo ha seleccionado el check de Guardar en Favoritos
            elif request.POST.get("favorite_check"):
                customed_register = Customed(title=film.title, description=film.description, time=film.time,
                                             genre=film.genre, image=film.image, release_date=film.release_date,
                                             user_id=request.user.id, category="Película", favorite=True)
                customed_register.save()

        # si ya existe un registro tipo Customed para esta película y usuario
        else:

            # Comprobación de que se ha rellenado correctamente el formulario
            if request.POST.get("seen_check") and request.POST.get("notSeen_check") or request.POST.get(
                    "favorite_check") and request.POST.get("notFavorite_check"):
                messages.warning(request, 'Opción no válida. Selecciona máximo dos opciones')
                return redirect('film_page', film_title, previous_url)

            # si se quiere marcar como Visto
            if request.POST.get("seen_check"):
                # actualizamos el registro de la base de datos
                Customed.objects.filter(title=film.title, user_id=request.user.id).update(seen=True)

            # si se quiere desmarcar el Visto
            if request.POST.get("notSeen_check"):
                Customed.objects.filter(title=film.title, user_id=request.user.id).update(seen=False)

            # si se quiere guardar en Favoritos
            if request.POST.get("favorite_check"):
                Customed.objects.filter(title=film.title, user_id=request.user.id).update(favorite=True)

            # si se quiere quitar de Favoritos
            if request.POST.get("notFavorite_check"):
                Customed.objects.filter(title=film.title, user_id=request.user.id).update(favorite=False)

        # actualizamos la página
        return redirect('film_page', film_title, previous_url)

    # Eliminar registro de la base de datos en caso de que el usuario lo desmarque como Visto y lo quite de Favoritos.
    # customed es un QuerySet object (lista con todos los registros obtenidos en esa consulta a la DB). En nuestro caso,
    # hemos asegurado que no haya registros duplicados -> customed solo tiene un registro (element)
    for element in customed:
        if not element.seen and not element.favorite:
            customed.delete()

    # ya podemos renderizar la página individual de esa película 'film_page.html'
    return render(request, 'film_page.html', {
        'film': film,
        'customed': customed,
        'back_url': back_url
    })

# vista para la página individual de cada serie (Prácticamente lo mismo que la vista film_page)
@login_required(login_url="login")
def series_page(request, series_title, previous_url):

    if previous_url == 'back_to_films':
        back_url = 'http://127.0.0.1:8000/peliculas/'
    elif previous_url == 'back_to_series':
        back_url = 'http://127.0.0.1:8000/series/'
    elif previous_url == 'back_to_favorites':
        back_url = 'http://127.0.0.1:8000/favoritos/'
    elif previous_url == 'back_to_seeAgain':
        back_url = 'http://127.0.0.1:8000/volver-a-ver/'

    # obtenemos la instancia de la serie en cuestión
    series = Series.objects.get(title=series_title)

    # obtenemos la instancia de contenido por usuario para saber si ya la ha marcado como visto o guardado en favoritos
    customed= Customed.objects.filter(title=series.title, user_id=request.user.id) # title=series_title=series.title

    # si llegan datos del formulario (marcado como visto y/o guardado en favoritos)
    if request.method == 'POST':

        # si aún no existe un registro tipo Customed para esta serie y usuario
        if not customed:

            # Comprobación de que se ha rellenado correctamente el formulario
            if request.POST.get("seen_check") and request.POST.get("notSeen_check") or request.POST.get(
                    "favorite_check") and request.POST.get("notFavorite_check") or request.POST.get(
                "notSeen_check") or request.POST.get("notFavorite_check"):
                messages.warning(request, 'Opción no válida. Selecciona máximo dos opciones')
                return redirect('series_page', series_title, previous_url)

            # si el usuario ha seleccionado los check de Visto y Guardar en Favoritos
            if request.POST.get("seen_check") and request.POST.get("favorite_check"):
                # creamos el nuevo registro y lo guardamos en la base de datos
                customed_register = Customed(title=series.title, description=series.description, seasons=series.seasons,
                                             episodes=series.episodes, time=series.time, genre=series.genre,
                                             image=series.image, release_date=series.release_date,
                                             user_id=request.user.id, category="Serie", seen=True, favorite=True)
                customed_register.save()

            # si el usuario solo ha seleccionado el check de Visto
            elif request.POST.get("seen_check"):
                customed_register = Customed(title=series.title, description=series.description, seasons=series.seasons,
                                             episodes=series.episodes, time=series.time, genre=series.genre,
                                             image=series.image, release_date=series.release_date,
                                             user_id=request.user.id, category="Serie", seen=True)
                customed_register.save()

            # si el usuario solo ha seleccionado el check de Guardar en Favoritos
            elif request.POST.get("favorite_check"):
                customed_register = Customed(title=series.title, description=series.description, seasons=series.seasons,
                                             episodes=series.episodes, time=series.time, genre=series.genre,
                                             image=series.image, release_date=series.release_date,
                                             user_id=request.user.id, category="Serie", favorite=True)
                customed_register.save()

        # si ya existe un registro tipo Customed para esta serie y usuario
        else:

            # Comprobación de que se ha rellenado correctamente el formulario
            if request.POST.get("seen_check") and request.POST.get("notSeen_check") or request.POST.get(
                    "favorite_check") and request.POST.get("notFavorite_check"):
                messages.warning(request, 'Opción no válida. Selecciona máximo dos opciones')
                return redirect('series_page', series_title, previous_url)

            # si se quiere marcar como Visto
            if request.POST.get("seen_check"):
                # actualizamos el registro de la base de datos
                Customed.objects.filter(title=series.title, user_id=request.user.id).update(seen=True)

            # si se quiere desmarcar el Visto
            if request.POST.get("notSeen_check"):
                Customed.objects.filter(title=series.title, user_id=request.user.id).update(seen=False)

            # si se quiere guardar en Favoritos
            if request.POST.get("favorite_check"):
                Customed.objects.filter(title=series.title, user_id=request.user.id).update(favorite=True)

            # si se quiere quitar de Favoritos
            if request.POST.get("notFavorite_check"):
                Customed.objects.filter(title=series.title, user_id=request.user.id).update(favorite=False)

        # actualizamos la página
        return redirect('series_page', series_title, previous_url)

    # Eliminar registro de la base de datos en caso de que el usuario lo desmarque como Visto y lo quite de Favoritos
    for element in customed:
        if not element.seen and not element.favorite:
            customed.delete()

    return render(request, 'series_page.html', {
        'series': series,
        'customed': customed,
        'back_url': back_url
    })

# vista para la página de series
@login_required(login_url="login")
def series(request):

    # búsqueda que ha escrito el usuario
    search = request.GET.get("buscar")

    # consultamos en la base de datos las series que hay
    series = Series.objects.all()

    # si el usuario está buscando algo
    if search:
        series = Series.objects.filter(
            Q(title__icontains = search) | Q(genre__icontains = search)
        )

    return render(request, 'series.html', {
        'title': 'Series',
        'series': series,
        'search': search
    })

# vista para la página de Favoritos
@login_required(login_url="login")
def favorites(request):

    # búsqueda que ha escrito el usuario
    search = request.GET.get("buscar")

    # Consultamos en la DB las películas y series que el usuario ha guardado en Favoritos
    favorite_content = Customed.objects.filter(user_id=request.user.id, favorite=True)

    # si el usuario está buscando algo
    if search:
        favorite_content = Customed.objects.filter(
            Q(title__icontains = search) & Q(user_id=request.user.id, favorite=True) |
            Q(genre__icontains=search) & Q(user_id=request.user.id, favorite=True)
        )

    return render(request, 'favorites.html', {
        'title': 'Favoritos',
        'favorite_content': favorite_content,
        'search': search
    })

# vista para la página de Volver a ver
@login_required(login_url="login")
def see_again(request):

    search = request.GET.get("buscar")

    # Consultamos en la DB las películas y series vistas por el usuario
    seen_content = Customed.objects.filter(user_id=request.user.id, seen=True)

    if search:
        seen_content = Customed.objects.filter(
            Q(title__icontains = search) & Q(user_id=request.user.id, seen=True) |
            Q(genre__icontains=search) & Q(user_id=request.user.id, seen=True)
        )

    return render(request, 'seeAgain.html', {
        'title': 'Volver a ver',
        'seen_content': seen_content,
        'search': search
    })

# vista para la página de Estadísticas
@login_required(login_url="login")
def statistics(request):

    # Si es el admin
    if request.user.is_superuser:

        clients = User.objects.exclude(is_superuser=True)

        # obtenemos la lista de usuarios
        clients_username = []
        for client in clients:
            clients_username.append(client.username)

        # obtenemos la lista de películas vistas por usuario
        clients_id = []
        for client in clients:
            clients_id.append(client.id)

        clients_seen_films = []
        for client in clients_id:
            seen_films = len(Customed.objects.filter(user_id=client, seen=True, category="Película"))
            clients_seen_films.append(seen_films)

        # obtenemos la lista de tiempo en horas visualizado en películas por usuario
        clients_time_seen_films = []
        for client in clients_id:
            client_seen_films = Customed.objects.filter(user_id=client, seen=True, category="Película")
            time = 0
            for film in client_seen_films:
                time += (film.time / 60)
            time = round(time, 1)
            clients_time_seen_films.append(time)

        # obtenemos la lista de series vistas por usuario
        clients_seen_series = []
        for client in clients_id:
            seen_series = len(Customed.objects.filter(user_id=client, seen=True, category="Serie"))
            clients_seen_series.append(seen_series)

        # obtenemos la lista de tiempo en horas visualizado en series por usuario
        clients_time_seen_series = []
        for client in clients_id:
            client_seen_series = Customed.objects.filter(user_id=client, seen=True, category="Serie")
            time = 0
            for film in client_seen_series:
                time += ((film.time / 60) * film.episodes)
            time = round(time, 1)
            clients_time_seen_series.append(time)

        return render(request, 'statistics.html', {
            'title': 'Estadísticas de los clientes',
            'clients_username': clients_username,
            'clients_seen_films': clients_seen_films,
            'clients_seen_series': clients_seen_series,
            'clients_time_seen_films': clients_time_seen_films,
            'clients_time_seen_series': clients_time_seen_series
        })

    # Si es un cliente
    else:
        # Consultamos los datos del usuario-cliente
        seen_films = Customed.objects.filter(user_id=request.user.id, seen=True, category="Película")

        seen_series = Customed.objects.filter(user_id=request.user.id, seen=True, category="Serie")

        # tiempo total de horas visualizado en películas por el cliente
        time_seen_films = 0
        for i in seen_films:
            time_seen_films += (i.time / 60)
        time_seen_films = round(time_seen_films, 1)

        # tiempo total de horas visualizado en series por el cliente
        time_seen_series = 0
        for i in seen_series:
            time_seen_series += ((i.time / 60) * i.episodes)
        time_seen_series = round(time_seen_series, 1)

        # Obtenemos los gráficos del cliente
        graph = get_hbar_graph(len(seen_films), len(seen_series))
        graph2 = get_hbar_graph2(time_seen_films, time_seen_series)

        return render(request, 'statistics.html', {
            'title': 'Estadísticas de usuario',
            'graph': graph,
            'graph2': graph2,
            'seen_films': len(seen_films),
            'seen_series': len(seen_series),
            'time_seen_films': time_seen_films,
            'time_seen_series': time_seen_series,
        })
