from django import template
register = template.Library()

@register.filter
def split(string,splitter):
    return string.split(splitter)

@register.filter
def lookup(d, key):
    return d[key]