# Project Pilgrims Hotel & Restaurant Website

A complete Django website for Project Pilgrims Hotel and Restaurant with a beautiful TailwindCSS design and warm beige/taupe color theme (#dabc94).

## Features

- Responsive design optimized for all device sizes
- Room booking and reservation system
- Restaurant menu display with filtering options
- Contact form
- About page with hotel history and team information
- Image galleries
- Reviews and testimonials
- TailwindCSS for styling
- Django 5.0 backend

## Technologies Used

- **Frontend**: HTML, CSS (TailwindCSS), JavaScript
- **Backend**: Python, Django 5.0
- **Database**: SQLite (development), PostgreSQL (recommended for production)
- **Dependencies**: See `requirements.txt`

## Installation Guide

### Prerequisites

- Python 3.9+
- Node.js and npm (for TailwindCSS)
- Git

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/project-pilgrims.git
cd project-pilgrims
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

5. **Set up TailwindCSS**

```bash
# Install Node.js dependencies
npm install

# Create a new Tailwind app
python manage.py tailwind init theme

# Install Tailwind dependencies
python manage.py tailwind install
```

6. **Set up environment variables**

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

7. **Run database migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

8. **Create a superuser**

```bash
python manage.py createsuperuser
```

9. **Start the development server**

```bash
# In one terminal, start the Tailwind CSS watcher
python manage.py tailwind start

# In another terminal, start the Django development server
python manage.py runserver
```

10. **Access the website**

Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.