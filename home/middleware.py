from django.utils.deprecation import MiddlewareMixin
from .models import VisitorCount


class VisitorCounterMiddleware(MiddlewareMixin):
    """
    Middleware to track unique visitors to the website.
    Uses session to ensure each visitor is counted only once per session.
    """

    def process_request(self, request):
        # Check if this visitor has already been counted in this session
        if not request.session.get('has_been_counted', False):
            # Increment the visitor count
            VisitorCount.increment()
            # Mark this session as counted
            request.session['has_been_counted'] = True

        return None
