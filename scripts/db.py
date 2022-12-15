"""Datastore Quickstart Example."""
import google.auth
from google.cloud import ndb

# Authenticate
credentials, project_id = google.auth.default()

# Initialize Client
client = ndb.Client()


# Model / Entity
class Book(ndb.Model):  # pylint: disable=too-few-public-methods
    """Example Model."""

    title = ndb.StringProperty()


# Execute queries within the NDB context.
def list_books():
    """Query for the Book entity."""
    with client.context():
        books = Book.query()
        for book in books:
            print(book.to_dict())


if __name__ == "__main__":
    print("Querying Books...")
    list_books()
