from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.generic import FormView
from django.urls import reverse_lazy #dependencia para la función reverse_lazy para el método CBV
from django.shortcuts import redirect, render #dependencia para la función redirect y render para el método FBV
#from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator #-> Dependencia para la creación de Eventos

from Final.apps.blog_auth.forms.models import Eventos
from posts.models import Usuario #Utilizo mi propio modelo definido en la app "posts"

class SignUpForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = {
            'username',
            'correo',
            'contrasenia',
            'contrasenia2'
        }


#-> Método CBV
class SignUpView(FormView):
    template_name = "registration/registrar.html"
    form_class = SignUpForm
    success_url = reverse_lazy("apps.blog_auth:login")

#-> Manejando la vista Login
class Login(auth_views.LoginView):
    template_name = "registration/login.html"

class EventoForm(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['titulo', 'descripcion', 'fecha', 'ubicacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type':'date'}),
        }

def form_valid(self, form):
    """ Verificamos que los datos sean válidos y los guadamos """
    form.save()
    return super().form_valid(form)

#-> Método FBV (que es el que usaré)
def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("apps.blog_auth:login")
    else:
        form = SignUpForm()
    return render(request, "registration/registrarhtml", {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        contrasenia = request.POST.get("password")
        user = authenticate(request, username=username, password=contrasenia)
        if user is not None:
            login(request, user)
            return redirect("apps.blog_auth:login")
        else:
            messages.error(request, "Credenciales incorrectas.")
    
    return render(request, "registration/login.html")

#-> | Creación de eventos FBV |

#-> Create View
def crear_evento(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_eventos")
    else:
        form = EventoForm()
    return render(request, "eventos/form_evento.html", {"form": form})

#-> Read Views
def listar_evento(request):
    eventos = Eventos.objects.all()

    query = request.GET.get('titulo', '')
    if query:
        eventos = eventos.filter(titulo__icontains=query)

    paginator = Paginator(eventos, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'eventos/lista_eventos.html', {'page_obj': page_obj, 'query': query})

#-> Read Views
def detalle_evento(request, id):
    try:
        evento = Eventos.objects.get(id=id)
    except Eventos.DoesNotExist:
        return HttpResponse("Evento no encontrado", status=404)
    
    return render(request, "eventos/detalle_evento.html", {"evento": evento})

#-> Update Views
def actualizar_evento(request, id):
    try:
        evento = Eventos.objects.get(id=id)
    except Eventos.DoesNotExist:
        return HttpResponse("Evento no encontrado", status=404)
    
    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect("lista_eventos", id=evento.id)
    else:
        form = EventoForm(instance=evento)
    
    return render(request, "eventos/form_evento.html", {'form': form, 'evento': evento})