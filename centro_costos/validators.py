from django.core.exceptions import ValidationError
import re

def validar_solo_letras(valor):
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', valor):
        raise ValidationError('Este campo solo debe contener letras y espacios.')