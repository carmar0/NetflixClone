from django.contrib import admin
from .models import Film, Series, Customed

# modelo para personalizar la visualización de los registros tipo Customed en el panel de administración
class CustomedAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'seen', 'favorite')  # para añadir esas columnas en la tabla de Contenido de usuario
    readonly_fields = ('user', 'title', 'description', 'seasons', 'episodes', 'time', 'genre', 'image', 'release_date', 'category', 'seen', 'favorite') # campos no modificable a través del panel admin
    ordering = ('-user',) # para ordenar la tabla de usuario más nuevo a más antiguo
    search_fields = ('title', 'category', 'user__username')  # para activar un buscador donde podamos buscar por titulo o nombre de usuario
    # user__username es el username guardado en el modelo User de django (poniendo user del modelo Customed puede dar error
    # debido al ForeignKey
    list_filter = ('user', 'title', 'category', 'seen', 'favorite') # para activar los filtros

# modelo para personalizar la visualización de los registros tipo Film en el panel de administración
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date')
    ordering = ('-release_date',)
    search_fields = ('title', 'genre', 'release_date')
    list_filter = ('genre', 'release_date')

# modelo para personalizar la visualización de los registros tipo Series en el panel de administración
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date')
    ordering = ('-release_date',)
    search_fields = ('title', 'genre', 'release_date')
    list_filter = ('genre', 'release_date')


# Configuración de títulos en el panel de administración
admin.site.site_header = "NETFLIX"
admin.site.site_title = "Netflix"  # la pestaña de la ventana
admin.site.index_title = "Panel de gestión"

# Register your models here.
admin.site.register(Film, FilmAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Customed, CustomedAdmin)

