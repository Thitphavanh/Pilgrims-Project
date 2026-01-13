from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset.select_related("category").prefetch_related("product_images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            context["current_category"] = get_object_or_404(Category, slug=category_slug)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.filter(is_available=True).select_related("category").prefetch_related("product_images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_products"] = Product.objects.filter(
            category=self.object.category, is_available=True
        ).exclude(pk=self.object.pk)[:4]
        return context


def product_list(request, category_slug=None):
    """Function-based view alternative"""
    products = Product.objects.filter(is_available=True).select_related("category").prefetch_related("product_images")
    categories = Category.objects.all()
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    context = {
        "products": products,
        "categories": categories,
        "current_category": current_category,
    }
    return render(request, "product/product_list.html", context)


def product_detail(request, slug):
    """Function-based view alternative"""
    product = get_object_or_404(
        Product.objects.filter(is_available=True).select_related("category").prefetch_related("product_images"),
        slug=slug
    )
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=product.pk)[:4]

    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "product/product_detail.html", context)
