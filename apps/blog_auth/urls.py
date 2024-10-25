from django.urls import path
from .views import login_view, register_view
from . import views

app_name = "apps.blog_auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path('', views.listar_evento, name='listar_eventos'),
    path('<int:id>/', views.detalle_evento, name='detalle_eventos'),
    path('crear/', views.crear_evento, name='crear_evento'),
    path('editar/<int:id>/', views.actualizar_evento, name='actualizar_evento'),
    path('eliminar/<int:id>/', views.eliminar_evento, name='eliminar_evento')
]