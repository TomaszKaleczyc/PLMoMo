from typing import Dict
from django.conf import settings


def app_version(request) -> Dict[str, str]:
    """
    Returns the app version for display
    """
    return {'app_version': f'v{settings.VERSION}'}
