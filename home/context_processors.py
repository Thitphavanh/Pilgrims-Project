from .models import VisitorCount


def visitor_count(request):
    """
    Context processor to make visitor count available in all templates.
    """
    return {
        'visitor_count': VisitorCount.get_count()
    }
