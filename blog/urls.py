from django.contrib import admin
from django.urls import path, include
from .views import index, pagina_404, nosotros  # Importamos desde views la función index
#URL LOGIN
from django.contrib.auth import views as auth

# Librerías para mostrar las imágenes de los posts (indica la ruta de la carpeta "media")
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import RedirectView # Redirige a la pagina principal (FEDE)
from.import views #FEDE

# Manejo de errores 404
handler404 = pagina_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # Página de inicio
    path('nosotros/', nosotros, name='nosotros'),  # Página de inosotros
    path('posts/', include('apps.posts.urls')),  # Incluye las URLs de los posts
    path('contacto/', include('apps.contacto.urls')),  # Incluye las URLs de contacto
    path('usuario/', include('apps.usuario.urls')),  # Incluye las URLs de usuario
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticación
    path('login/',auth.LoginView.as_view(template_name='usuarios/login.html'),name='login'),
    path('logout/',auth.LogoutView.as_view(next_page='/login'),name="logout"),
    path('accounts/profile/', RedirectView.as_view(url='/inicio/'), name='profile'), #fede
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()  # Servir archivos estáticos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Servir archivos multimedia