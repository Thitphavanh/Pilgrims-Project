# Translation Guide: Lao & English

This guide explains how to add bilingual support (Lao and English) for database content in your Django project.

## Understanding Translation Types

There are **two types** of translation in Django:

### 1. Static Text Translation (Using `{% trans %}`)
For **hardcoded text** in templates that never changes.

**Example:**
```django
{% trans "Welcome to our website" %}
{% trans "About Us" %}
{% trans "Contact" %}
```

**When to use:** Menu labels, button text, static headings, error messages.

### 2. Dynamic Database Content Translation (Using Database Fields)
For **content stored in the database** that changes.

**Example:**
```django
{{ category.name }}
{{ product.description }}
{{ room.title }}
```

**When to use:** Category names, product details, room descriptions, any user-generated content.

---

## How to Add Translations for Database Content

### Step 1: Add Translation Fields to Your Model

**Before:**
```python
class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
```

**After:**
```python
class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, help_text="Name in English")
    name_lo = models.CharField(max_length=100, blank=True, help_text="Name in Lao")

    def get_localized_name(self, language_code='en'):
        """Return the name in the requested language"""
        if language_code == 'lo' and self.name_lo:
            return self.name_lo
        return self.name
```

### Step 2: Create and Run Migration

```bash
# Create migration
docker compose exec web python manage.py makemigrations

# Apply migration
docker compose exec web python manage.py migrate
```

### Step 3: Update Templates

**Before:**
```django
<h1>{{ category.name }}</h1>
```

**After:**
```django
<h1>
    {% if LANGUAGE_CODE == 'lo' and category.name_lo %}
        {{ category.name_lo }}
    {% else %}
        {{ category.name }}
    {% endif %}
</h1>
```

### Step 4: Add Translations via Django Admin

1. Go to Django Admin: `http://localhost:8000/admin/`
2. Find your model (e.g., Gallery Categories)
3. Edit each record and fill in the Lao field
4. Save

---

## Examples by Model

### Gallery Categories

**Fields:**
- `name` (English) - "Restaurant"
- `name_lo` (Lao) - "ຮ້ານອາຫານ"

**Template Usage:**
```django
{% if LANGUAGE_CODE == 'lo' and category.name_lo %}
    {{ category.name_lo }}
{% else %}
    {{ category.name }}
{% endif %}
```

### Gallery Images

**Fields:**
- `title` (English) - "Delicious Breakfast"
- `title_lo` (Lao) - "ອາຫານເຊົ້າແຊບໆ"
- `description` (English) - "Fresh breakfast served daily"
- `description_lo` (Lao) - "ອາຫານເຊົ້າສົດໃໝ່ທຸກວັນ"

**Template Usage (with Alpine.js):**
```django
<!-- For displaying title -->
{% if LANGUAGE_CODE == 'lo' and image.title_lo %}
    {{ image.title_lo }}
{% else %}
    {{ image.title }}
{% endif %}

<!-- For passing to Alpine.js (must escape) -->
@click="title = '{% if LANGUAGE_CODE == 'lo' and image.title_lo %}{{ image.title_lo|escapejs }}{% else %}{{ image.title|escapejs }}{% endif %}'"
```

### Menu Categories (Already Implemented)

The `MenuCategory` model already has this pattern built-in with a `get_category_display()` method that returns translated names.

**Example Categories:**
- coffee → "Coffee" / "ກາເຟ"
- breakfast → "Breakfast" / "ອາຫານເຊົ້າ"
- drinks → "Drinks" / "ເຄື່ອງດື່ມ"

---

## Common Patterns

### Pattern 1: Simple Field Translation
```django
{% if LANGUAGE_CODE == 'lo' and object.field_lo %}
    {{ object.field_lo }}
{% else %}
    {{ object.field }}
{% endif %}
```

### Pattern 2: Using Helper Method
```python
# In model
def get_localized_field(self):
    from django.utils.translation import get_language
    lang = get_language()
    if lang == 'lo' and self.field_lo:
        return self.field_lo
    return self.field
```

```django
<!-- In template -->
{{ object.get_localized_field }}
```

### Pattern 3: In Title/Meta Tags (One Line)
```django
{% block title %}{% if LANGUAGE_CODE == 'lo' and category.name_lo %}{{ category.name_lo }}{% else %}{{ category.name }}{% endif %}{% endblock %}
```

---

## Files Updated in This Project

### 1. Gallery App
**Model:** `gallery/models.py`
- Added `name_lo` field to `GalleryCategory`
- Added `title_lo` and `description_lo` fields to `GalleryImage`
- Added `get_localized_name()`, `get_localized_title()`, and `get_localized_description()` helper methods

**Templates:**
- `templates/base.html` - Desktop & mobile gallery dropdowns (lines 176-182, 264-270)
- `gallery/templates/gallery/gallery_image_list.html` - Page title, heading, image titles, and descriptions (lines 5, 9-15, 20-29)

### 2. Restaurant App
**Model:** `restaurant/models.py`
- `MenuCategory` uses built-in translation system

**Template Usage:**
```django
{{ category.name }}  <!-- Already translates automatically -->
```

---

## Translation Checklist

When adding a new translatable field:

- [ ] Add `field_lo` to model
- [ ] Add helper text: `help_text="Name in Lao"`
- [ ] Make it optional: `blank=True`
- [ ] Create migration: `python manage.py makemigrations`
- [ ] Run migration: `python manage.py migrate`
- [ ] Update all templates using that field
- [ ] Add translations via Django admin
- [ ] Test language switching on frontend

---

## Common Mistakes to Avoid

### ❌ Wrong: Using `{% trans %}` with Variables
```django
{% trans "{{ category.name }}" %}  <!-- DOES NOT WORK -->
{% trans category.name %}          <!-- DOES NOT WORK -->
```

### ✅ Correct: Using Conditional Logic
```django
{% if LANGUAGE_CODE == 'lo' and category.name_lo %}
    {{ category.name_lo }}
{% else %}
    {{ category.name }}
{% endif %}
```

---

## Testing Translations

1. **Switch Language:** Use the language toggle in the header
2. **Check Database:** Ensure Lao fields are filled in Django admin
3. **Verify Fallback:** If Lao field is empty, it should show English
4. **Test All Pages:** Check each page where the field appears

---

## Need Help?

If you encounter translation issues:

1. Check if the field has `_lo` suffix in the model
2. Verify migration was applied: `python manage.py showmigrations`
3. Check Django admin to ensure Lao translation exists
4. Verify template uses conditional logic (not `{% trans %}`)

---

## Future Improvements

Consider using **django-modeltranslation** or **django-parler** for:
- Automatic translation field generation
- Admin interface improvements
- Cleaner template syntax
- Support for more languages

For now, the manual approach works well for 2 languages (Lao + English).
