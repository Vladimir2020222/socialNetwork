from django import template

register = template.Library()


@register.filter(name='enumerate')
def do_enumerate(value):
    return enumerate(value)
