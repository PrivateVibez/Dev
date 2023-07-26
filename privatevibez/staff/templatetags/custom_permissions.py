from django import template
from django.contrib.auth.models import Permission

register = template.Library()

@register.filter
def has_permission(user, permission_name):
    try:
        permission = Permission.objects.get(codename=permission_name)
        staff = Staff.object.get(staff_id_id=user)
        return user.has_perm(permission)
    except Permission.DoesNotExist:
        return False