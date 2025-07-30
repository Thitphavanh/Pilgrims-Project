from .models import ReviewSummary

def review_summary(request):
    """Add review summary to all template contexts"""
    try:
        summary = ReviewSummary.objects.first()
        if not summary:
            summary = ReviewSummary.objects.create()
        return {'review_summary': summary}
    except:
        return {'review_summary': None}