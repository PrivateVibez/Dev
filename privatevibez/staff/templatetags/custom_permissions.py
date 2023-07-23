from django import template
from django.contrib.auth.models import Permission

register = template.Library()

@register.filter
def has_permission(user, permission_name):
    try:
        permission = Permission.objects.get(codename=permission_name)
        return user.has_perm(permission)
    except Permission.DoesNotExist:
        return False