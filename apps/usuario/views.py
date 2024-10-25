from apps.usuario.models import Usuario
from apps.posts.models import Comentario, Post
from .forms import RegistroUsuarioForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group

class RegistrarUsuario(CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'registration/registrar.html'
    success_url = reverse_lazy('login')  # Redirigir después del registro exitoso

    def form_valid(self, form):
        # Guarda el formulario y crea el usuario
        user = form.save()
        # Obtener o crear el grupo si no existe
        group, created = Group.objects.get_or_create(name='Registrado')  # Verifica o crea el grupo 'Registrado'
        user.groups.add(group)  # Asigna al usuario recién creado al grupo
        return super().form_valid(form)  # Continúa con el proceso normal de validación

    def form_invalid(self, form):
        """
        Si el formulario no es válido, muestra un mensaje de error.
        """
        messages.error(self.request, 'Error en el registro. Por favor, corrige los errores.')
        return super().form_invalid(form)

# Vista para el inicio de sesión de usuario
class LoginUsuario(LoginView):
    template_name = 'usuario/loguin.html'
    form_class = LoginForm  # Usa el formulario personalizado de login

    def get_success_url(self):
        """
        Una vez que el usuario inicia sesión correctamente, redirige a la lista de usuarios
        y muestra un mensaje de éxito.
        """
        messages.success(self.request, 'Login exitoso.')
        return reverse('apps.usuario:usuario_list')

# Vista para cerrar sesión de usuario
class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'

    def get_success_url(self):
        """
        Al cerrar la sesión, muestra un mensaje de éxito y redirige al login.
        """
        messages.success(self.request, "¡Sesión cerrada correctamente!")
        return reverse('apps.usuario:login')

# Vista para listar los usuarios registrados, excluyendo superusuarios
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'registration/usuario_list.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        """
        Excluye a los superusuarios de la lista de usuarios.
        """
        queryset = super().get_queryset()
        queryset = queryset.exclude(is_superuser=True)
        return queryset

# Vista para eliminar un usuario, con opción de eliminar también sus comentarios y posts
class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'registration/eliminar_usuario.html'
    success_url = reverse_lazy('apps.usuario:usuario_list')

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto, como si el usuario es parte del grupo 'Colaborador'.
        """
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Colaborador')
        es_colaborador = colaborador_group in self.object.groups.all()
        context['es_colaborador'] = es_colaborador
        return context

    def post(self, request, *args, **kwargs):
        """
        Permite eliminar los comentarios y posts asociados al usuario antes de eliminarlo.
        Muestra un mensaje de éxito al finalizar.
        """
        eliminar_comentarios = request.POST.get('eliminar_comentarios', False)
        eliminar_posts = request.POST.get('eliminar_posts', False)
        self.object = self.get_object()

        if eliminar_comentarios:
            Comentario.objects.filter(usuario=self.object).delete()  # Elimina comentarios del usuario

        if eliminar_posts:
            Post.objects.filter(autor=self.object).delete()  # Elimina posts del usuario

        messages.success(request, f'Usuario {self.object.username} eliminado correctamente')
        return self.delete(request, *args, **kwargs)
