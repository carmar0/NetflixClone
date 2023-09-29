from django.db import models

# editor de texto enriquecido (hemos instalado previamente la librería ckeditor: "pip install django-ckeditor")
from ckeditor.fields import RichTextField

# importamos el modelo de Usuario que viene por defecto con Django para el panel de administración de la web
from django.contrib.auth.models import User


# Create your models here.

# Esto son los modelos para representar/crear las tablas de nuestra base de datos SQLite3. Cada instancia/objeto
# (una película, una serie, un Customed) del modelo representa una fila de la tabla y cada propiedad de la clase
# una columna

# modelo para la tabla de películas
class Film(models.Model):
    title = models.CharField(max_length=80, verbose_name='Título')
    # verbose_name es el nombre de la columna que aparece en la tabla del panel de administración
    description = RichTextField(max_length=650, verbose_name='Sinopsis')
    time = models.IntegerField(verbose_name='Duración')
    genre_options = [
        ("Acción", "Acción"),
        ("Aventuras", "Aventuras"),
        ("Ciencia Ficción", "Ciencia Ficción"),
        ("Comedia", "Comedia"),
        ("Drama", "Drama"),
        ("Fantástico", "Fantástico"),
        ("Musical", "Musical"),
        ("Suspense", "Suspense"),
        ("Thriller", "Thriller"),
        ("Terror", "Terror"),
        ("Bélico", "Bélico"),
        ("Policíaco", "Policíaco"),
        ("Histórico", "Histórico"),
        ("Western", "Western"),
        ("Deportivo", "Deportivo"),
        ("Animación", "Animación"),
    ]
    genre = models.CharField(max_length=15, verbose_name='Género', choices=genre_options)
    image = models.ImageField(default='nul', verbose_name="Portada", upload_to="media/Películas") # las imágenes se guardan en la carpeta "media" del proyecto
    release_date = models.IntegerField(verbose_name='Año de estreno')

    class Meta:
        verbose_name = 'Película'
        verbose_name_plural = 'Películas'
        ordering = ['-release_date'] # para que los ordene en orden descendiente de fecha de estreno

    def __str__(self):
        return self.title

# modelo para la tabla de series
class Series(models.Model):
    title = models.CharField(max_length=80, verbose_name='Título')
    description = RichTextField(max_length=650, verbose_name='Sinopsis')
    seasons = models.IntegerField(verbose_name='Temporadas')
    episodes = models.IntegerField(verbose_name='Episodios')
    time = models.IntegerField(verbose_name='Duración')
    genre_options = [
        ("Acción", "Acción"),
        ("Aventuras", "Aventuras"),
        ("Ciencia Ficción", "Ciencia Ficción"),
        ("Comedia", "Comedia"),
        ("Drama", "Drama"),
        ("Fantástico", "Fantástico"),
        ("Musical", "Musical"),
        ("Suspense", "Suspense"),
        ("Thriller", "Thriller"),
        ("Terror", "Terror"),
        ("Bélico", "Bélico"),
        ("Policíaco", "Policíaco"),
        ("Histórico", "Histórico"),
        ("Western", "Western"),
        ("Deportivo", "Deportivo"),
        ("Animación", "Animación"),
    ]
    genre = models.CharField(max_length=15, verbose_name='Género', choices=genre_options)
    image = models.ImageField(default='nul', verbose_name="Portada", upload_to="media/Series")
    release_date = models.IntegerField(verbose_name='Año de estreno')

    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'
        ordering = ['-release_date']

    def __str__(self):
        return self.title

# modelo para la tabla de series y películas por usuario (para ver cuáles tiene marcadas como vistas y favoritas)
class Customed(models.Model):
    title = models.CharField(max_length=80, verbose_name='Título')
    description = RichTextField(max_length=650, verbose_name='Sinopsis')
    seasons = models.IntegerField(verbose_name='Temporadas', default=0)
    episodes = models.IntegerField(verbose_name='Episodios', default=0)
    time = models.IntegerField(verbose_name='Duración')
    genre = models.CharField(max_length=15, verbose_name='Género')
    image = models.ImageField(default='nul', verbose_name="Portada")
    release_date = models.IntegerField(verbose_name='Año de estreno')

    user = models.ForeignKey(User, editable=False, verbose_name='Usuario', on_delete=models.CASCADE)
    # de esta manera relacionamos la propiedad user con el id del modelo User que se haya creado en la base de datos
    # on_delete=models.CASCADE -> si un usuario se elimina, también se eliminarán sus registros de esta tabla
    # editable=False para que no se pueda seleccionar qué usuario está personalizando su contenido (visto y/o Favorito)

    category = models.CharField(max_length=8, verbose_name="Categoría")
    seen = models.BooleanField(default=False, verbose_name='¿Vista?')
    favorite = models.BooleanField(default=False, verbose_name='¿Favorita?')

    class Meta:
        verbose_name = 'Contenido de usuario'
        verbose_name_plural = 'Contenido de usuarios'


"""
 Una vez definidos los modelos o cada vez que se haga algún cambio en ellos, hay que migrarlos a la base de datos 
 (se crearán las tablas en la base de datos):
 
    1) python manage.py makemigrations
    2) python manage.py sqlmigrate content NumberOfMigration -> esto crea el código SQL correspondiente a las tablas de
        esos modelos
    3) python manage.py migrate -> esto migra finalmente ese código a la base de datos
    
 A continuación habrá que añadir estos modelos a admin.py para que aparezcan en el panel de administración de nuestra web
"""