from django import template
register = template.Library()

@register.filter
def split(string,splitter):
    return string.split(splitter)