# Django and mongo-datatables Demo

A minimal, elegant demo showcasing the integration of [mongo-datatables](https://github.com/MongoDataTables/mongo-datatables) with Django 5.0.3.

## Features

- Single page application with a clean, modern UI
- MongoDB integration with DataTables for server-side processing
- Support for nested document fields
- Full CRUD operations via DataTables Editor (optional)
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

## Using DataTables Editor

This demo is configured to work with or without DataTables Editor. By default, the Editor functionality is disabled to allow users to run the demo without requiring a commercial license.

To enable the Editor functionality:

1. Purchase and download DataTables Editor from [https://editor.datatables.net/](https://editor.datatables.net/)

2. Place the Editor files in the static directory:
   ```
   dystopia/books/static/Editor-2.4.1/
   ```

3. Uncomment the Editor CSS and JavaScript imports in `dystopia/books/templates/books/index.html`:
   ```html
   <!-- Uncomment these lines -->
   <link href="{% static 'Editor-2.4.1/css/editor.bootstrap5.min.css' %}" rel="stylesheet">
   <script src="{% static 'Editor-2.4.1/js/dataTables.editor.min.js' %}"></script>
   <script src="{% static 'Editor-2.4.1/js/editor.bootstrap5.min.js' %}"></script>
   ```

4. Refresh the page, and you'll now have full CRUD capabilities with the Editor interface

The application will automatically detect if the Editor scripts are loaded and enable the appropriate functionality.

## Technologies

- Django 5.0.3
- mongo-datatables 1.1.1
- jQuery DataTables 2.2.2
- Bootstrap 5
- MongoDB
- DataTables Editor 2.4.1 (optional)

## Project Structure

The project follows a minimalist approach with just the essential components:

- `models.py`: Simple MongoDB connection and collection wrapper
- `views.py`: Three focused views for the main page and API endpoints
- `urls.py`: Clean routing for the main page and API endpoints
- `index.html`: Single template with integrated DataTable and Editor

## mongo-datatables

Find mongo-datatables at [https://github.com/MongoDataTables/mongo-datatables](https://github.com/MongoDataTables/mongo-datatables).

[![Downloads](http://pepy.tech/badge/mongo-datatables)](http://pepy.tech/project/mongo-datatables)

## Support

If you find this project helpful, consider buying me a coffee!

<a href="https://www.buymeacoffee.com/pjosols" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


