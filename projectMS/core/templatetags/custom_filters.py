from django.template import Library

register = Library()

@register.filter(name='str_split')
def str_split(value:str, char:str):
    return value.split(char)

@register.filter(name='divide')
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.filter(name='multiply')
def multiply(value1, value2):
    # you would need to do any localization of the result here
    return value1 * value2