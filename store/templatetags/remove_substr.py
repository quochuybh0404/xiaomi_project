from django import template
import re

register = template.Library()

@register.filter
def remove_substr(string,char):
    return string.replace(char, '')

@register.filter
def split_string(string, arg):
    return string.split(arg)

@register.filter
def string_concat(string, arg):
    list_string =  split_string(string, arg)
    new_str = list_string[0] + '_' + list_string[1]
    return new_str