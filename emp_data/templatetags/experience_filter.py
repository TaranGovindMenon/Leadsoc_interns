from django import template
register = template.Library()

@register.filter
def change_to_true(value):
    return True

register.app_name = 'emp_data'
