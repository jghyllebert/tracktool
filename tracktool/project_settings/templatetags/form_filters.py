from django import template
register = template.Library()


@register.filter('field_type')
def get_field_type(field):
    return field.field.widget.__class__.__name__