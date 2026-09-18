from django.urls import path
from . import views

urlpatterns = [
    
    path("temblor/", views.temblor, name="formulario_temblor"),
    path("salida-temblor/", views.salida_temblor, name="resultado"),
    path('lista-temblores/', views.lista_temblores, name='lista_temblores'),
    path('buscar-temblor/', views.buscar_temblor, name='buscar_temblor'),
]