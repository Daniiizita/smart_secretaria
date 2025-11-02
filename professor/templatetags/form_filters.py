from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """
    Adiciona classe CSS a um BoundField de forma segura.
    Se value não for BoundField tenta usar as_widget, caso contrário retorna value.
    """
    try:
        if isinstance(value, BoundField):
            widget = value.field.widget
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = (existing + ' ' + css_class).strip() if existing else css_class
            return value
        return value.as_widget(attrs={'class': css_class})
    except Exception:
        return value