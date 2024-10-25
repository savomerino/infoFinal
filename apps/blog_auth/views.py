from django.http import HttpResponse
from django.urls import reverse_lazy #dependencia para la función reverse_lazy para el método CBV
from django.shortcuts import redirect, render #dependencia para la función redirect y render para el método FBV
from django.core.paginator import Paginator #-> Dependencia para la creación de Eventos

from Final.apps.blog_auth.forms.forms import EventoForm
from Final.apps.blog_auth.forms.models import Eventos
from posts.models import Usuario #Utilizo mi propio modelo definido en la app "posts"

# Create your views here.

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

#-> Delete Views
def eliminar_evento(request, id):
    try:
        evento = Eventos.objects.get(id=id)
    except Eventos.DoesNotExist:
        return HttpResponse("Evento no encontrado", status=404)

    if request.method == 'POST':
        evento.delete()
        return redirect("lista_eventos")

    return render(request, "eventos/confirmacion_eliminacion.html", {"evento": evento})
