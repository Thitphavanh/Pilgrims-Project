
from django.shortcuts import render, get_object_or_404
from .models import GalleryCategory, GalleryImage

def gallery_category_list(request):
    categories = GalleryCategory.objects.all()
    return render(request, 'gallery/gallery_category_list.html', {'categories': categories})

def gallery_image_list(request, category_slug):
    category = get_object_or_404(GalleryCategory, slug=category_slug)
    images = GalleryImage.objects.filter(category=category)
    return render(request, 'gallery/gallery_image_list.html', {'category': category, 'images': images})

