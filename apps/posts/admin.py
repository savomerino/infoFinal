from django.contrib import admin
from .models import Colaborador
from .models import Usuario
from .models import Comentario
from .models import Categoria
from .models import Post

# Register your models here.
#admin.site.register(Colaborador)
#admin.site.register(Usuario)
admin.site.register(Comentario)
admin.site.register(Categoria)
admin.site.register(Post)