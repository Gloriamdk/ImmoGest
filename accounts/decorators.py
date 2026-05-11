from django.contrib.auth.decorators import user_passes_test


def proprietaire_required(view_func):
    """
    Autorise uniquement les propriétaires.
    """
    decorator = user_passes_test(
        lambda user: user.is_authenticated and user.role == 'proprietaire'
    )

    return decorator(view_func)


def locataire_required(view_func):
    """
    Autorise uniquement les locataires.
    """
    decorator = user_passes_test(
        lambda user: user.is_authenticated and user.role == 'locataire'
    )

    return decorator(view_func)