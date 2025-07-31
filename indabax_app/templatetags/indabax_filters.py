# indabax_app/templatetags/indabax_filters.py
from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def divide_int(value, arg):
    try:
        return int(int(value) / int(arg))
    except (ValueError, ZeroDivisionError):
        return None
    
@register.filter
def split_lines(value):
    """
    Splits a string by newline characters and returns a list of lines.
    """
    if not isinstance(value, str):
        return []
    return value.splitlines()

@register.filter
def strip(value):
    """
    Strips whitespace from the beginning and end of a string.
    """
    if not isinstance(value, str):
        return value
    return value.strip()