from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def paciente_required():
    def in_group(user):
        if user.is_authenticated:
            if (hasattr(user, 'paciente') and user.paciente.groups.name == "Paciente"):
                return True
            else:
                raise PermissionDenied
        return False

    return user_passes_test(in_group)