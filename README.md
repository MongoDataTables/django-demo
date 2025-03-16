# Django and mongo-datatables Demo

A minimal, elegant demo showcasing the integration of [mongo-datatables](https://github.com/MongoDataTables/mongo-datatables) with Django 5.0.3.

## Features

- Single page application with a clean, modern UI
- MongoDB integration with DataTables for server-side processing
- Support for nested document fields
- Full CRUD operations via DataTables Editor
- Export functionality (Excel, CSV, PDF)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Seed the database with sample data:

```bash
python seed_data.py --count 100
```

3. Run the development server:

```bash
cd mysite
python manage.py runserver
```

4. Open your browser and navigate to http://localhost:8000

## Technologies

- Django 5.0.3
- mongo-datatables 1.0.1
- jQuery DataTables 2.2.2
- Bootstrap 5
- MongoDB

## Project Structure

The project follows a minimalist approach with just the essential components:

- `models.py`: Simple MongoDB connection and collection wrapper
- `views.py`: Three focused views for the main page and API endpoints
- `urls.py`: Clean routing for the main page and API endpoints
- `index.html`: Single template with integrated DataTable and Editor

## mongo-datatables

Find mongo-datatables at [https://github.com/MongoDataTables/mongo-datatables](https://github.com/MongoDataTables/mongo-datatables).

[![Downloads](http://pepy.tech/badge/mongo-datatables)](http://pepy.tech/project/mongo-datatables)



