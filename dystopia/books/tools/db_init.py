# books/tools/db_init.py
from pymongo import MongoClient
from django.conf import settings


def create_indexes(db=None):
    """
    Create MongoDB indexes for optimal performance with large collections.
    
    This function creates text indexes for search capabilities and regular indexes
    for sorting and filtering operations. It's crucial for performance with large
    collections (e.g., 2M records).
    
    Args:
        db: MongoDB database instance. If None, a new connection will be established.
    """
    try:
        # Use the provided db or create a new connection
        if db is None:
            client = MongoClient('localhost', 27017)
            db = client['book_database']

        print("Creating MongoDB indexes...")
        
        # Create text indexes for full-text search capabilities
        db["books"].create_index([
            ('Title', 'text'),
            ('Author', 'text'),
            ('Description', 'text'),
            ('Themes', 'text')  # Added Themes array for text search
        ])

        # Create regular indexes for sorting/filtering
        # Basic fields
        db["books"].create_index('NovelId')
        db["books"].create_index('Title')
        db["books"].create_index('Author')
        db["books"].create_index('Pages')
        db["books"].create_index('Rating')
        db["books"].create_index('Themes')

        # Nested fields
        db["books"].create_index('PublisherInfo.Date')  # Important for date filtering

        print("MongoDB indexes created successfully!")

    except Exception as e:
        print(f"Error creating indexes: {e}")
        import traceback
        print(traceback.format_exc())


def main():
    """
    Run as standalone script to create indexes manually.
    
    This function allows the script to be run directly to create indexes
    without going through the Django initialization process.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Create MongoDB indexes for book database')
    parser.add_argument('--uri', type=str, default='mongodb://localhost:27017/book_database',
                      help='MongoDB connection string (default: mongodb://localhost:27017/book_database)')

    args = parser.parse_args()

    # Connect directly to MongoDB
    client = MongoClient(args.uri)
    db = client.get_database()

    print(f"Connected to MongoDB: {args.uri}")
    create_indexes(db)


if __name__ == "__main__":
    # This will be executed when running as python -m books.tools.db_init
    main()
