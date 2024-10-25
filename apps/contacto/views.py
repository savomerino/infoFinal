from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

class ContactoUsuario(CreateView):
    template_name = 'contacto/contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('contacto:contacto')  # Redirige a la vista 'contacto'.

    def get_context_data(self, **kwargs):
        # Añade el objeto 'request' al contexto para posibles usos en la plantilla.
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

    def form_valid(self, form):
        # Muestra un mensaje de éxito cuando el formulario se envía correctamente.
        messages.success(self.request, 'Consulta enviada.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Añade el 'request' a los argumentos del formulario, útil si quieres acceder al usuario autenticado.
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        # Si quieres que la URL de éxito dependa del objeto creado (ej. ID del contacto), lo puedes manejar aquí.
        return reverse_lazy('contacto:contacto')
    
    
    def form_send_email(self, form):
        # Aquí podrías separar la lógica de enviar correos para mantener la vista limpia.
        # Por ejemplo, podrías acceder a los datos del formulario y enviarlos por correo.
        pass
