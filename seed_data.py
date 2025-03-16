from pymongo import MongoClient
from faker import Faker
from datetime import datetime
import random
import uuid
import time
import argparse
import os
import django

# Set up Django environment
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'dystopia'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dystopia.settings')
django.setup()


def generate_books(count, batch_size=1000, connection_string='mongodb://localhost:27017/'):
    """Generate unique book records and insert them into MongoDB."""
    # Initialize Faker
    fake = Faker()

    # Connect to MongoDB
    print(f"Connecting to MongoDB at {connection_string}")
    client = MongoClient(connection_string)
    db = client['book_database']
    collection = db['books']

    # Clear existing data
    print("Clearing existing data...")
    collection.delete_many({})

    # Lists for generating dystopian themes (kept from original)
    themes = [
        "Environmental collapse", "Surveillance state", "Artificial intelligence takeover",
        "Post-apocalyptic survival", "Totalitarian government", "Corporate control",
        "Biological warfare aftermath", "Digital consciousness", "Class warfare",
        "Genetic engineering", "Mind control", "Resource depletion", "Technological dependence",
        "Social media dystopia", "Reality manipulation", "Memory erasure", "Pandemic aftermath",
        "Climate disaster", "Robotic revolution", "Virtual reality imprisonment"
    ]

    # Publisher information (kept from original)
    publishers = [
        "Dystopian Press", "Future Books", "New World Publishing",
        "Horizon Press", "Nightfall Books", "Digital Age Publishers",
        "Apocalypse Media", "Broken Mirror Publishing", "Synthetic Press",
        "Echo Publishers", "Dark Sky Books", "Neon Ink Press",
        "Carbon Echo Books", "Algorithm Publishing", "Memory Lane Press"
    ]

    publisher_locations = [
        "New York", "London", "Tokyo", "Berlin", "Sydney", "Toronto",
        "Paris", "Seoul", "San Francisco", "Mexico City", "Stockholm",
        "Singapore", "Mumbai", "Cape Town", "Barcelona"
    ]

    ratings = [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    # Setup for tracking progress
    start_time = time.time()
    last_update = start_time
    books_inserted = 0

    print(f"Beginning generation of {count} books in batches of {batch_size}...")

    # Batch processing
    for i in range(0, count, batch_size):
        batch = []
        batch_size = min(batch_size, count - i)

        for j in range(batch_size):
            # Create unique title using a randomly selected method
            title_methods = [
                lambda: fake.catch_phrase().title(),
                lambda: " ".join(fake.words(nb=random.randint(2, 5))).title(),
                lambda: f"The {fake.word().title()} Of {fake.word().title()}",
                lambda: f"{fake.word().title()} {fake.word().title()}",
                lambda: f"{fake.word().title()}: {' '.join(fake.words(nb=random.randint(2, 4))).title()}"
            ]

            # Select and execute a random title generation method
            title = random.choice(title_methods)()

            # Create unique author
            author = fake.name()

            # Generate random publication date between 1950 and 2024
            year = random.randint(1950, 2024)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            pub_date = datetime(year, month, day)

            # Create the nested PublisherInfo object
            publisher_info = {
                'Name': random.choice(publishers),
                'Date': pub_date,
                'Location': random.choice(publisher_locations),
                'Edition': random.randint(1, 5),
                'Details': {
                    'ISBN': f"978-{random.randint(1000000000, 9999999999)}",
                    'Format': random.choice(["Hardcover", "Paperback", "eBook", "Audiobook"]),
                    'PrintRun': random.randint(1000, 50000)
                }
            }

            # Generate page count
            pages = random.randint(180, 800)

            # Select themes - between 1 and 3 unique themes
            novel_themes = random.sample(themes, random.randint(1, 3))

            # Rating
            rating = random.choice(ratings)

            # Description - same as original
            theme_text = " and ".join(novel_themes).lower()
            descriptions = [
                f"A haunting exploration of {theme_text} in a world where humanity's future hangs by a thread.",
                f"When society collapsed, the only thing left was {theme_text}. A stark warning of what might come.",
                f"Set in a future where {theme_text} has forever changed what it means to be human.",
                f"A chilling narrative exploring {theme_text} and the resilience of the human spirit.",
                f"In the aftermath of {theme_text}, one person's journey reveals the dark truth of our present."
            ]
            description = random.choice(descriptions)

            # Create a unique ID
            novel_id = f"DYST-{uuid.uuid4().hex[:8].upper()}"

            batch.append({
                'NovelId': novel_id,
                'Title': title,
                'Author': author,
                'PublisherInfo': publisher_info,
                'Pages': pages,
                'Themes': novel_themes,
                'Rating': rating,
                'Description': description
            })

        # Insert batch into MongoDB
        if batch:
            result = collection.insert_many(batch)
            books_inserted += len(result.inserted_ids)

        # Show progress every 10 seconds or each million records
        current_time = time.time()
        if current_time - last_update > 10 or (books_inserted % 1000000) < batch_size:
            elapsed = current_time - start_time
            books_per_second = books_inserted / elapsed if elapsed > 0 else 0
            percent_complete = (books_inserted / count) * 100

            # Estimate time remaining
            if books_per_second > 0:
                remaining_books = count - books_inserted
                seconds_remaining = remaining_books / books_per_second
                minutes_remaining = seconds_remaining / 60
                if minutes_remaining < 1:
                    time_remaining = f"{int(seconds_remaining)} seconds"
                elif minutes_remaining < 60:
                    time_remaining = f"{int(minutes_remaining)} minutes"
                else:
                    time_remaining = f"{int(minutes_remaining / 60)} hours, {int(minutes_remaining % 60)} minutes"
            else:
                time_remaining = "calculating..."

            print(f"Progress: {books_inserted:,}/{count:,} books ({percent_complete:.1f}%) | "
                  f"Speed: {books_per_second:.1f} books/sec | Est. time remaining: {time_remaining}")

            last_update = current_time

    # Final stats
    total_time = time.time() - start_time
    print(f"\nCompleted! Generated {books_inserted:,} unique books in {total_time:.1f} seconds")
    print(f"Average insertion rate: {books_inserted / total_time:.1f} books/second")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate book records for MongoDB')
    parser.add_argument('--count', type=int, default=100,
                        help='Number of book records to generate (default: 100)')
    parser.add_argument('--batch-size', type=int, default=1000,
                        help='Batch size for MongoDB inserts (default: 1000)')
    parser.add_argument('--connection', type=str, default='mongodb://localhost:27017/',
                        help='MongoDB connection string (default: mongodb://localhost:27017/)')

    args = parser.parse_args()

    try:
        # Check if Faker is installed
        import faker
    except ImportError:
        print("The Faker package is not installed. Installing now...")
        import subprocess
        import sys

        subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
        import faker

    generate_books(args.count, args.batch_size, args.connection)
