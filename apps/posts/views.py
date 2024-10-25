from .models import Comentario, Post, Categoria
from .forms import ComentarioForm, CrearPostForm, NuevaCategoriaForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

# VISTA DE INICIO: Renderiza los 3 posts más recientes en la página principal
# Esta vista es útil para la página de inicio del sitio web
def index(request):
    posts = Post.objects.all().order_by('-fecha_publicacion')[:3]
    print(posts)  # Verifica que los posts sean correctos
    return render(request, 'index.html', {'posts': posts})

# VISTA DE LISTA DE POSTS BASADA EN FUNCIONES: Lista todos los posts en el sitio
# Usar esta vista es simple y directa para manejar plantillas
def posts(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})

# VISTA DE LISTA DE POSTS BASADA EN FUNCIONES (con otro template)
# Similar a la anterior, pero posiblemente apuntando a un template diferente
def lista_posts(request):
    posts = Post.objects.all()
    return render(request, 'tu_template.html', {'posts': posts})

# CLASE PostListView: Vista basada en clases que lista posts
# Esta vista utiliza una ListView genérica, lo que facilita la paginación, ordenación y reuso
class PostListView(ListView):
    model = Post
    template_name = "posts/posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        # Método para obtener la lista de posts, con la opción de ordenarlos por fecha o alfabéticamente
        queryset = super().get_queryset()
        orden = self.request.GET.get('orden')
        if orden == 'reciente':
            queryset = queryset.order_by('-fecha')
        elif orden == 'antiguo':
            queryset = queryset.order_by('fecha')
        elif orden == 'alfabetico':
            queryset = queryset.order_by('titulo')
        return queryset
    
    def get_context_data(self, **kwargs):
        # Provee datos adicionales al contexto (como el orden elegido por el usuario)
        context = super().get_context_data(**kwargs)
        context['orden'] = self.request.GET.get('orden', 'reciente')
        return context

# CLASE PostDetailView: Detalle de un post específico
# Muestra la información de un post individual y maneja la lógica para agregar comentarios
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_individual.html"
    context_object_name = "posts"
    pk_url_kwarg = "id"
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        # Agrega el formulario de comentarios y los comentarios relacionados al contexto de la vista
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['comentarios'] = Comentario.objects.filter(posts_id=self.kwargs['id'])
        return context
    
    def post(self, request, *args, **kwargs):
        # Maneja el envío del formulario de comentarios
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.posts_id = self.kwargs['id']
            comentario.save()
            return redirect('apps.posts:post_individual', id=self.kwargs['id'])
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

# CLASE PostCreateView: Crear un post nuevo (requiere login)
# Permite a los usuarios registrados crear nuevos posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('apps.posts:posts')

# CLASE PostUpdateView: Modificar un post existente
# Permite a los usuarios actualizar un post que ya han creado
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = CrearPostForm
    template_name = 'posts/modificar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

# CLASE PostDeleteView: Eliminar un post
# Los usuarios pueden eliminar un post; la vista redirige a la lista de posts después de la eliminación
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/eliminar_post.html'
    success_url = reverse_lazy('apps.posts:posts')

# CLASE PostsPorCategoriaView: Listar posts por categoría
# Filtra los posts según una categoría específica
class PostsPorCategoriaView(ListView):
    model = Post
    template_name = 'posts/posts_por_categoria.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(categoria_id=self.kwargs['pk'])

# CLASE CategoriaCreateView: Crear una nueva categoría (requiere login)
# Permite a los usuarios registrados agregar nuevas categorías de posts
class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = NuevaCategoriaForm
    template_name = 'posts/crear_categoria.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.posts:crear_post')

# CLASE CategoriaListView: Lista todas las categorías
# Simplemente muestra una lista de todas las categorías existentes
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'posts/categoria_list.html'
    context_object_name = 'categorias'

# CLASE CategoriaDeleteView: Eliminar una categoría (requiere login)
# Permite eliminar una categoría específica y redirige a la lista de categorías tras la eliminación
class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'posts/categoria_confirm_delete.html'
    success_url = reverse_lazy('apps.posts:categoria_list')

# CLASE ComentarioCreateView: Crear un comentario para un post
# Vista que permite a los usuarios agregar comentarios a los posts
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/agregarComentario.html'
    success_url = 'comentario/comentarios/'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.posts_id = self.kwargs['posts_id']
        return super().form_valid(form)

# CLASE ComentarioUpdateView: Editar un comentario
# Los usuarios pueden modificar los comentarios que ya han dejado
class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentario/comentario_form.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('apps.posts:post_individual', args=[self.object.posts.id])

# CLASE ComentarioDeleteView: Eliminar un comentario
# Los usuarios pueden eliminar comentarios que han hecho
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentario/comentario_confirm_delete.html'

    def get_success_url(self):
        return reverse('apps.posts:post_individual', args=[self.object.posts.id])
