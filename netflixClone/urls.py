"""
URL configuration for netflixClone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainApp.urls')),   # añadimos las url de la aplicación mainApp
    path('', include('content.urls'))   # añadimos las url de la aplicación content
]

# Ruta para visualizar las imágenes
if settings.DEBUG: # si el proyecto está en modo debug
    from django.conf.urls.static import static
    # creamos una ruta para cargar las imágenes en nuestro servidor local
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # document_root es la ruta absoluta de nuestro directorio media donde se guardaran las imágenes