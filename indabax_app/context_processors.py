# indabax_app/context_processors.py
from .models import SiteSettings

def indabax_settings(request): # <--- RENAMED THE FUNCTION
    try:
        # Attempt to get the first (and presumably only) SiteSettings object
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    return {'indabax_settings': settings} # <--- RENAMED THE DICTIONARY KEY