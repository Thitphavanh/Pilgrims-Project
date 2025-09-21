# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Docker Development Workflow
```bash
# Start development environment
docker-compose up --build

# Run database migrations (in new terminal)
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell

# Run management commands
docker-compose exec web python manage.py <command_name>
```

### Data Management Commands
```bash
# Seed restaurant menu with sample items
docker-compose exec web python manage.py seed_menu_items

# Setup review platforms (Agoda, Booking.com, Airbnb)
docker-compose exec web python manage.py setup_review_platforms

# Import sample hotel reviews
docker-compose exec web python manage.py import_sample_reviews

# Load drinks menu data
docker-compose exec web python manage.py load_drinks_menu

# Update translation files
docker-compose exec web python manage.py update_translations
```

### Testing
```bash
# Run all tests
docker-compose exec web python manage.py test

# Run specific app tests
docker-compose exec web python manage.py test hotel
docker-compose exec web python manage.py test restaurant
```

## Architecture Overview

### Multi-App Django Structure
- **pilgrims/**: Main project with split settings (dev/prod/base)
- **home/**: Landing page, contact forms, main navigation
- **hotel/**: Complex booking system with rooms, amenities, and review aggregation
- **restaurant/**: Menu management with multi-category support
- **coffee/**: Coffee shop specific features

### Database Design
**Hotel System** (`hotel/models.py`):
- `RoomType`: Room categories with pricing and amenities
- `Room`: Individual rooms with availability and maintenance tracking
- `Amenity`: Room features with icon/color customization
- `RoomAmenity`: Through model linking rooms to amenities with additional info
- `Booking`: Reservation system with status tracking
- **Review System**: Multi-platform review aggregation (Agoda, Booking.com, Airbnb)
  - `ReviewPlatform`: Different review platforms with branding
  - `PlatformRating`: Overall ratings per platform
  - `CategoryRating`: Category-specific ratings (Service, Cleanliness, etc.)
  - `GuestReview`: Individual reviews with trip type tracking

**Restaurant System** (`restaurant/models.py`):
- `MenuItem`: Menu items with categories, pricing, and multilingual support
- Supports 9 categories: breakfast, coffee, american, indian, drinks, mexican, pizza, local_food, soup_salad_mediterranean
- Auto-generates slugs for SEO-friendly URLs

### Internationalization
- Supports English (en) and Lao (lo) languages
- Uses Django's i18n framework with `LocaleMiddleware`
- Menu categories have Lao translations
- URL patterns use `i18n_patterns` for language prefixes

### Settings Configuration
- **Base settings**: Common configuration in `pilgrims/settings/base.py`
- **Development**: `DJANGO_SETTINGS_MODULE=pilgrims.settings.dev`
- **Production**: Uses production settings with Gunicorn
- PostgreSQL database with environment variable configuration

### Static Files & Media
- Static files collected to `staticfiles/` directory
- Media uploads stored in `media/` directory
- Uses WhiteNoise for static file serving
- TailwindCSS for styling with beige/taupe theme (#dabc94)

## Key Model Relationships

### Hotel Booking Flow
1. `RoomType` defines room categories with base pricing
2. `Room` instances belong to room types and have specific amenities
3. `RoomAmenity` through model adds room-specific amenity details
4. `Booking` links guests to specific rooms with date ranges
5. Review system aggregates ratings from multiple platforms

### Restaurant Menu System
- Menu items are categorized and support featured items
- Automatic slug generation for SEO
- Multi-language category support
- Price stored in LAK (Lao Kip)

### Review Platform Integration
- Supports major booking platforms (Agoda, Booking.com, Airbnb)
- Each platform has custom branding (colors, logos)
- Category ratings vary by platform (e.g., Airbnb uses different categories)
- Automatic calculation of overall ratings weighted by review count

## Container & Deployment

### Development Environment
- Uses `docker-compose.yml` with PostgreSQL database
- Includes Adminer for database management (port 8080)
- Live code reloading with volume mounts

### Production Environment
- Uses `docker-compose.prod.yml` with Gunicorn
- Optimized Dockerfile with static file collection
- Production settings with appropriate security configurations

## Environment Variables
Copy `.env.example` to `.env` and configure:
- `SECRET_KEY`: Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASS`: PostgreSQL credentials
- `DEBUG`: Set to 1 for development, 0 for production
- `ALLOWED_HOSTS`: Comma-separated hosts for production