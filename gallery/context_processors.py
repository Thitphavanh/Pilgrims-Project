from .models import GalleryCategory

def gallery_categories(request):
    return {
        'gallery_categories': GalleryCategory.objects.all()
    }
