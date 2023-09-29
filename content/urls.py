from django.urls import path
from . import views

urlpatterns = [
    path('peliculas/', views.films, name="films"),
    path('pelicula/<str:film_title>/<str:previous_url>/', views.film_page, name="film_page"),
    path('series/', views.series, name="series"),
    path('serie/<str:series_title>/<str:previous_url>/', views.series_page, name="series_page"),
    path('favoritos/', views.favorites, name="favorites"),
    path('volver-a-ver/', views.see_again, name="see_again"),
    path('estadisticas/', views.statistics, name="statistics")
]