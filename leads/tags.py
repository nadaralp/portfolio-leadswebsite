from django import template

register = template.Library()

@register.simple_tag
def active(request, pathname):
    # import re
    # if re.search(pathname, request.path):
    if request.path.replace("/", "") == pathname:
        return 'active'
    return ''