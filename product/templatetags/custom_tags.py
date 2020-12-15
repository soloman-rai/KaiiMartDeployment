from django import template


register = template.Library()

# Tags for comments
@register.filter(name='get_val')
def get_val(dict,key):
    return dict.get(key)

# Tags for similar products ratings
@register.filter(name='get_checked_range')
def get_checked_range(value, arg):
    return range(arg)

@register.filter(name='get_unchecked_range')
def get_unchecked_range(value, arg):
    return range(5-arg)    


