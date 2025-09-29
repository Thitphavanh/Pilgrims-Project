from django import template

register = template.Library()

@register.filter
def lao_intcomma(value):
    """
    Format numbers with commas for both English and Lao locales.
    Works similar to Django's intcomma but handles Lao formatting.
    """
    if not value:
        return value

    try:
        # Convert to string if it's a number
        if isinstance(value, (int, float)):
            value = str(int(value))
        else:
            value = str(value)

        # Remove any existing commas or spaces
        value = value.replace(',', '').replace(' ', '').replace('LAK', '').strip()

        # Convert to integer for formatting
        number = int(float(value))

        # Format with commas
        formatted = f"{number:,}"

        return formatted

    except (ValueError, TypeError):
        return value

@register.filter
def lao_currency(value):
    """
    Format currency for Lao locale with proper comma separation.
    """
    formatted_number = lao_intcomma(value)
    return f"{formatted_number} LAK"