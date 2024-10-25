from django.urls import path
from .import views

app_name = 'contacto'  # Correcto: el nombre de la app es 'contacto'

urlpatterns = [
    path('contacto/', views.ContactoUsuario.as_view(), name='contacto'),  # Corregido: el nombre es 'contacto'
]
