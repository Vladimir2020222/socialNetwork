from django import template

register = template.Library()


@register.filter(name='enumerate')
def do_enumerate(value):
    return enumerate(value)


@register.filter(name='mul')
def mul(a, b):
    return a * b
