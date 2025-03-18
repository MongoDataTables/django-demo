# MongoDB DataTables Django Demo

A comprehensive demonstration application showcasing the integration of MongoDB with jQuery DataTables for efficient server-side processing, built using Django 5.0.3.

## About This Project

This demo application illustrates how to use the `mongo-datatables` Python package to connect MongoDB collections with DataTables, enabling powerful server-side processing for large datasets with minimal configuration.

The demo presents a fictional "Dystopian Archives" database to showcase various features including:

- Server-side pagination, sorting, and filtering
- Global search across multiple fields
- Column-specific searches
- Support for nested document structures
- Type-aware search operations (dates, numbers, text, etc.)
- Proper handling of MongoDB data types
- Optimized text search using MongoDB text indexes
- Advanced schema system with field type definitions
- Class-based views with dynamic schema support

## Prerequisites

- Python 3.9.6+
- MongoDB 5.0+ (running locally or accessible via network)
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/MongoDataTables/django-demo.git
   cd django-demo
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. **Important:** DataTables Editor is a commercial product and is not included in this repository.
   - If you wish to enable the editing features, purchase a license from [DataTables Editor](https://editor.datatables.net/)
   - Download and place the Editor files in `dystopia/books/static/books/Editor-2.4.1/`
   - Uncomment the Editor-related lines in the HTML templates

## Seeding Data

To test and demonstrate the functionality of this application, you'll need sample data in your MongoDB database. The project includes a data seeding script that generates sample book records with dystopian themes.

### Basic Usage

```bash
# Generate 100 sample books (default)
python seed_data.py --count 100

# Generate a specific number of books
python seed_data.py --count 1000

# Use a custom MongoDB connection string
python seed_data.py --connection "mongodb://username:password@hostname:port/"
```

### Data Structure

The seeding script creates book records with the following structure:

```javascript
{
  "NovelId": "DYST-1A2B3C4D",       // Unique identifier
  "Title": "The Last Horizon",       // Book title
  "Author": "Alex Zhang",            // Author name
  "PublisherInfo": {                 // Nested publisher information
    "Name": "Dystopian Press",
    "Date": ISODate("2022-03-15"),
    "Location": "New York",
    "Edition": 2,
    "Details": {
      "ISBN": "978-1234567890",
      "Format": "Hardcover",
      "PrintRun": 25000
    }
  },
  "Pages": 324,                      // Page count
  "Themes": [                        // Array of themes
    "Environmental collapse", 
    "Post-apocalyptic survival"
  ],
  "Rating": 4.5,                     // Book rating
  "Description": "A haunting exploration of environmental collapse..."
}
```

This structure demonstrates many MongoDB capabilities including nested documents and arrays, making it perfect for testing the DataTables and Editor integration.

## Running the Application

Start the development server:
```
python manage.py runserver
```

The application will be available at [http://localhost:8000](http://localhost:8000)

## Using DataTables Editor

This demo is configured to work with or without DataTables Editor. By default, the Editor functionality is disabled to allow users to run the demo without requiring a commercial license.

To enable the Editor functionality:

1. Purchase and download DataTables Editor from [https://editor.datatables.net/](https://editor.datatables.net/)

2. Place the Editor files in the static directory:
   ```
   dystopia/books/static/books/Editor-2.4.1/
   ```

3. Uncomment the Editor CSS and JavaScript imports in `dystopia/books/templates/books/index.html`:
   ```html
   <!-- Uncomment these lines -->
   <link href="{% static 'books/Editor-2.4.1/css/editor.bootstrap5.min.css' %}" rel="stylesheet">
   <script src="{% static 'books/Editor-2.4.1/js/dataTables.editor.min.js' %}"></script>
   <script src="{% static 'books/Editor-2.4.1/js/editor.bootstrap5.min.js' %}"></script>
   ```

4. Refresh the page, and you'll now have full CRUD capabilities with the Editor interface

The application will automatically detect if the Editor scripts are loaded and enable the appropriate functionality.

## Advanced Features

### Optimized MongoDB Text Search

The project includes an `OptimizedDataTables` class that extends the original `DataTables` class to leverage MongoDB text indexes for improved search performance:

- Uses MongoDB text search instead of regex searches when available
- Provides detailed query statistics for debugging
- Maintains compatibility with the original DataTables implementation
- Handles both simple and complex search terms

### Advanced Schema System

The project features a comprehensive schema system that:

- Captures the complete MongoDB document structure including nested fields
- Defines proper types for all fields including deep nested paths like 'PublisherInfo.Details.ISBN'
- Supports special MongoDB types like 'objectid'
- Separates schema definition from UI display concerns with DISPLAY_FIELDS dictionary
- Uses smart field type selection for different views

### Class-Based Views with Dynamic Schema Support

The project uses class-based views with dynamic schema support:

- `CollectionSchema` class in models.py defines field types for different collections
- `DataTablesView` and `EditorView` class-based views dynamically determine field types based on collection name
- Maintains backward compatibility with function-based views that delegate to the class-based views

## Project Structure

```
django-demo/
├── dystopia/                 # Main Django project
│   ├── books/                # Books app
│   │   ├── static/           # Static files (CSS, JS, etc.)
│   │   │   └── books/        # App-specific static files
│   │   ├── templates/        # Templates
│   │   │   └── books/        # App-specific templates
│   │   ├── tools/            # Utility tools for the books app
│   │   ├── __init__.py       # Python package indicator
│   │   ├── apps.py           # Django app configuration
│   │   ├── models.py         # MongoDB models and schema definitions
│   │   ├── urls.py           # URL routing for the books app
│   │   └── views.py          # View functions and classes
│   ├── dystopia/             # Project settings
│   │   ├── __init__.py       # Python package indicator
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py           # Main URL routing
│   │   └── wsgi.py           # WSGI application entry point
│   ├── static/               # Collected static files for production
│   └── manage.py             # Django management script
├── .gitignore                # Git ignore configuration
├── seed_data.py              # Data seeding script for MongoDB
└── requirements.txt          # Python dependencies
```

## Technologies

- Django 5.0.3
- mongo-datatables 1.1.1
- jQuery DataTables 2.2.2
- Bootstrap 5
- MongoDB
- DataTables Editor 2.4.1 (optional)

## mongo-datatables

Find mongo-datatables at [https://github.com/MongoDataTables/mongo-datatables](https://github.com/MongoDataTables/mongo-datatables).

[![Downloads](http://pepy.tech/badge/mongo-datatables)](http://pepy.tech/project/mongo-datatables)

## Support

If you find this project helpful, consider buying me a coffee!

<a href="https://www.buymeacoffee.com/pjosols" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

