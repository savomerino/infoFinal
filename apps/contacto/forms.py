from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto  # Reemplaza 'Contacto' con el nombre correcto de tu modelo
        fields = ['nombre_apellido', 'email', 'asunto', 'mensaje']

    def __init__(self, *args, **kwargs):
        # Extraemos el 'request' de kwargs para usarlo si es necesario
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)