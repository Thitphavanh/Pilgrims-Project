# Project Pilgrims Hotel & Restaurant Website

A complete Django website for Project Pilgrims Hotel and Restaurant with a beautiful TailwindCSS design and warm beige/taupe color theme (#dabc94). This project is fully containerized with Docker for easy and consistent development and deployment.

Got it. Here is the clean version of the project tree without the comments, ready to be added to your `README.md`.

-----

##  Project Structure

```
Pilgrims-Project/
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── manage.py
├── README.md
├── requirements.txt
│
├── coffee/
├── home/
├── hotel/
├── restaurant/
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── staticfiles/
├── media/
├── templates/
└── locale/
```

## Features

-   Responsive design optimized for all device sizes
-   Room booking and reservation system
-   Restaurant menu display with filtering options
-   Contact form and about page
-   Image galleries, reviews, and testimonials
-   Fully containerized for simple setup and deployment

---

## Technologies & Tools

-   **Backend**: Python, Django 5.x
-   **Frontend**: TailwindCSS, HTML, JavaScript
-   **Database**: PostgreSQL
-   **Containerization**: Docker, Docker Compose
-   **Web Server**: Gunicorn (for production environment)

---

## 🚀 Local Development Setup with Docker

This project uses Docker to streamline the setup process. You no longer need to install Python, Node.js, or PostgreSQL locally.

### Prerequisites

-   Git
-   Docker & Docker Compose

### Step-by-Step Guide

1.  **📂 Clone the Repository**
    Clone the project to your local machine.
    ```bash
    git clone [https://github.com/yourusername/project-pilgrims.git](https://github.com/yourusername/project-pilgrims.git)
    cd project-pilgrims
    ```

2.  **🔑 Set Up Environment Variables**
    Create your local environment file by copying the provided example. The default values are already configured for the Docker setup.
    ```bash
    cp .env.example .env
    ```

3.  **🛠️ Build and Run the Containers**
    This single command builds the Docker images, starts the Django and PostgreSQL services, and shows you the application logs.
    ```bash
    docker compose up --build
    ```
    Keep this terminal running.

4.  **🗄️ Run Database Migrations**
    The first time you start the application, you need to set up the database schema. **Open a new terminal window** and run:
    ```bash
    docker compose exec web python manage.py migrate
    ```

5.  **🧑‍💻 Create a Superuser (Optional)**
    To access the Django admin panel, create an administrator account. In the second terminal, run:
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

---

## ✅ Accessing the Application

-   **Website**: Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
-   **Admin Panel**: Navigate to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## Production Deployment

A production-ready `docker-compose.prod.yml` file is included. To run the application in a detached production mode, use the following command:

```bash
docker-compose -f docker-compose.prod.yml up --build -d