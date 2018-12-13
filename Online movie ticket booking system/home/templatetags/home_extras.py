from django import template

register = template.Library()


@register.filter()
def modulo(a, b):
    i = int(a) % int(b)
    return i
