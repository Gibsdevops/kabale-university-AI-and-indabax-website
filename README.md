Project Structure
This Django web application, IndabaX Kabale AI Club, is organized into a main project and several distinct Django applications, each handling specific functionalities.

indabax_kabale/ # Django project root

├── indabax_kabale/ # Project-level settings and configurations
│ ├── settings.py # Main settings file
│ ├── urls.py # Root URL dispatcher
│ ├── wsgi.py / asgi.py # For deployment
│ └── init.py
├── kuai_club/ # Main app for Kabale University AI Club
│ ├── templates/kuai_club/ # Templates (home, about, community list)
│ ├── static/kuai_club/ # Static files (CSS, images)
│ ├── models.py # Site-wide models (e.g., Community list)
│ ├── views.py # Views for home, about, communities
│ ├── urls.py # App-specific URLs
│ └── admin.py, apps.py, etc.

├── indabax_app/ # App for IndabaX Kabale AI Club (sub-community)
│ ├── templates/indabax_app/ # IndabaX pages (home, tutorials, leaders)
│ ├── static/core/ # Static files (CSS, JS, images)
│ ├── models.py # IndabaX models (Leader, Tutorial)
│ ├── views.py # Views for IndabaX pages
│ ├── urls.py # IndabaX-specific routes
│ └── admin.py, apps.py, etc.

├── media/ # Uploaded media (e.g. leader images)
├── staticfiles/ # Collected static files for deployment
├── manage.py # Django management utility
├── db.sqlite3 # SQLite DB (dev environment)
├── Pipfile / requirements.txt # Dependency management (Pipenv/pip)

Explanation of Key Directories/Files:
indabax_kabale/ (Outer Project Folder): This is the root of your Django project. It contains manage.py and the main project configuration folder.

indabax_kabale/ (Inner Project Folder): This folder holds the core settings and the root URL configuration for your entire Django project.

settings.py: Defines database connections, installed applications, static/media file locations, and other global configurations.

urls.py: This is the master URL file that includes URL patterns from your individual apps.

kuai_club/ and indabax_app/: These are individual Django applications. Each app is designed to handle a specific set of features or content (e.g., kuai_club for core club info, indabax_app for IndabaX specific content like tutorials/leaders).

migrations/: Stores database migration files that Django uses to track and apply changes to your database schema.

static/: Contains static assets like CSS, JavaScript, and images that are part of the app itself. Each app's static files are namespaced (e.g., kuai_club/static/kuai_club/).

templates/: Stores the HTML template files for rendering web pages. Templates are also namespaced (e.g., kuai_club/templates/kuai_club/).

models.py: Defines the database tables (models) and their relationships for the app.

views.py: Contains the logic that processes web requests, interacts with models, and renders appropriate templates.

urls.py: Defines URL patterns specific to the app, which are then included in the project's root urls.py.

admin.py: Configures how the app's models are displayed and managed in the Django administration interface.

media/: This directory is where user-uploaded content (like profile pictures, event photos, etc.) is stored.

staticfiles/: This directory is created when you run python manage.py collectstatic. It's where all static files from all your apps and Django's admin are collected into a single location, ready for serving in a production environment.

db.sqlite3: The default SQLite database file used during development.

manage.py: A command-line utility that lets you interact with your Django project (e.g., runserver, makemigrations, migrate, collectstatic).

Pipfile, Pipfile.lock: Files used by Pipenv for managing project dependencies, ensuring consistent environments.
