import pytest
from app import create_app, db
from models import User, Book, ReadingEvent
from services import stats_service, reading_service
from datetime import datetime, timedelta, timezone

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_calculate_streak(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.flush()

        book = Book(title="Test Book", author="Author", pages=100, genre="test", added_by=user.id)
        db.session.add(book)
        db.session.flush()

        now = datetime.now(timezone.utc)

        # Finished today, yesterday, and day before
        events = [
            ReadingEvent(user_id=user.id, book_id=book.id, started_at=now-timedelta(days=10), finished_at=now),
            ReadingEvent(user_id=user.id, book_id=book.id, started_at=now-timedelta(days=10), finished_at=now-timedelta(days=1)),
            ReadingEvent(user_id=user.id, book_id=book.id, started_at=now-timedelta(days=10), finished_at=now-timedelta(days=2)),
        ]
        # We need unique books because of UniqueConstraint if we were using different books,
        # but here I'm using the same book_id which might violate UniqueConstraint if I'm not careful.
        # Actually seed_data uses unique user_id/book_id.

        # Let's create unique books to be safe and realistic
        books = [
            Book(title=f"Book {i}", author="Author", pages=100, genre="test", added_by=user.id)
            for i in range(3)
        ]
        db.session.add_all(books)
        db.session.flush()

        events = [
            ReadingEvent(user_id=user.id, book_id=books[0].id, started_at=now-timedelta(days=10), finished_at=now),
            ReadingEvent(user_id=user.id, book_id=books[1].id, started_at=now-timedelta(days=10), finished_at=now-timedelta(days=1)),
            ReadingEvent(user_id=user.id, book_id=books[2].id, started_at=now-timedelta(days=10), finished_at=now-timedelta(days=2)),
        ]
        db.session.add_all(events)
        db.session.commit()

        streak = stats_service.calculate_streak(user.id)
        assert streak == 3

def test_history_sorting(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.flush()

        books = [
            Book(title=f"Book {i}", author="Author", pages=100, genre="test", added_by=user.id)
            for i in range(2)
        ]
        db.session.add_all(books)
        db.session.flush()

        now = datetime.now(timezone.utc)
        # Book 1 started LATER but finished EARLIER
        # Book 0 started EARLIER but finished LATER
        e0 = ReadingEvent(user_id=user.id, book_id=books[0].id, started_at=now-timedelta(days=5), finished_at=now-timedelta(days=1))
        e1 = ReadingEvent(user_id=user.id, book_id=books[1].id, started_at=now-timedelta(days=2), finished_at=now-timedelta(days=3))

        db.session.add_all([e0, e1])
        db.session.commit()

        history = reading_service.get_reading_history(user.id)
        # Expected order: most recently finished first.
        # e0 finished 1 day ago, e1 finished 3 days ago.
        # So e0 should be first.
        assert history[0].book_id == books[0].id
        assert history[1].book_id == books[1].id
