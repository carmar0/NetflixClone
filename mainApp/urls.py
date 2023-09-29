from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('inicio/', views.index, name="inicio"),
    path('registrarse/', views.register, name="register"),
    path('acceder/', views.log_in, name="login"),
    path('cerrar-sesion/', views.log_out, name="logout"),
    path('admin/', views.admin, name="admin")
]