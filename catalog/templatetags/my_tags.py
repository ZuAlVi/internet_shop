from django import template

register = template.Library()


@register.filter()
def media_filter(value):
    if value:
        return f'/media/{value}'

    return '/static/img/No_photo.jpeg'


@register.simple_tag()
def media_tag(value):
    if value:
        return f'/media/{value}'

    return '/static/img/No_photo.jpeg'
