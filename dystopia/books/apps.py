from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

    def ready(self):
        """
        Method called when the Django app is ready.
        This is the perfect place to run initialization code like creating MongoDB indexes.
        """
        # Import inside the method to avoid circular imports
        from pymongo import MongoClient
        from .tools.db_init import create_indexes
        
        # Only run in the main process, not in management commands or other subprocesses
        import sys
        import os
        
        # Check if this is the main process (not the auto-reloader)
        # RUN_MAIN is set by Django's auto-reloader in the spawned child process
        if not os.environ.get('RUN_MAIN', False) and ('runserver' in sys.argv or 'gunicorn' in sys.argv[0]):
            try:
                logger.info("Checking MongoDB connection and creating indexes...")
                client = MongoClient('localhost', 27017)
                db = client['book_database']
                
                # Ping the database to check connection
                db.command('ping')
                logger.info("MongoDB connected successfully!")
                
                # Create indexes
                create_indexes(db)
            except Exception as e:
                logger.error(f"MongoDB connection error: {e}")
