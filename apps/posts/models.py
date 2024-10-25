from django.db import models
from django.utils import timezone
from django.conf import settings

from apps.usuario.models import Usuario

# Create your models here.

#=============================================================================#
#-> Modelo de Comentarios para los Posts
#=============================================================================#

class Comentario(models.Model):
    posts = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.texto

#=============================================================================#
#-> Modelos para los Posts
#=============================================================================#

#Colaborador
class Colaborador(models.Model):
    correo = models.CharField(max_length=40, null=False)
    username = models.CharField(max_length=25, null=False)
    contrasenia = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.username

#Usuario Registrado
""" class Usuario(models.Model):
    correo = models.CharField(max_length=40, null=False)
    username = models.CharField(max_length=25, null=False)
    contrasenia = models.CharField(max_length=30, null=False)
    administrado = models.ManyToManyField(Colaborador, blank=True)

    def __str__(self):
        return self.username """

#Comentario
""" class Comentario(models.Model):
    texto = models.TextField(null=False)
    usuario_FK = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    valoraciones = models.IntegerField(null=True)
    administrado = models.ManyToManyField(Colaborador, blank=True, through='ADMINxCOMENTARIO') """


#Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=30, null= False)

    def __str__(self):
        return self.nombre

#Post
class Post(models.Model):
    titulo = models.CharField(max_length=50, null=False)
    subtitulo = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(null=False)
    activo = models.BooleanField(default=True)
    #usuario_FK = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, default='sin categoría')
    imagen = models.ImageField(null=True, blank=True, upload_to='media', default='static/post_default.png')
    publicado = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    #administrado = models.ManyToManyField(Colaborador, blank=True)

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return self.titulo
    
    def delete(self, using = None, keep_parents = False):
        self.imagen.delete(self.imagen.name)
        super().delete()

#Tablas intermedias -> Modelos para los campos ManyToMany de los modelos Usuario, Comentario y Post
""" class ADMINxUSUARIO(models.Model):
    id_colaborador_FK = models.ForeignKey(Colaborador, on_delete=models.CASCADE, blank=True, null=True)
    id_usuario_FK = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    accion = models.CharField(max_length=20, null=True)
    descripcion = models.TextField(null=True)

class ADMINxPOST(models.Model):
    id_colaborador_FK = models.ForeignKey(Colaborador, on_delete=models.CASCADE, blank=True, null=True)
    id_post_FK = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    accion = models.CharField(max_length=20, null=True)
    descripcion = models.TextField(null=True)

class ADMINxCOMENTARIO(models.Model):
    id_colaborador_FK = models.ForeignKey(Colaborador, on_delete=models.CASCADE, blank=True, null=True)
    id_comentario_FK = models.ForeignKey(Comentario, on_delete=models.CASCADE, blank=True, null=True)
    accion = models.CharField(max_length=20, null=True)
    descripcion = models.TextField(null=True) """