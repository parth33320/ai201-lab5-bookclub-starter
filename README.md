# BookClub — Tinker 5 (Elite Engineering Edition)

A small reading list app where club members track books, log their progress, and see their reading stats.

## What the app does

- **Book list** — members add books to a shared reading list
- **Reading tracker** — mark books as started or finished
- **Stats** — reading streak, books finished this month, total pages read

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows

pip install -r requirements.txt

python seed_data.py    # populate the database
python app.py          # start the server (runs at http://127.0.0.1:5000)
```

## API

| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/books/`                       | List all books                       |
| POST   | `/books/`                       | Add a book                           |
| POST   | `/reading/start`                | Mark a book as started               |
| POST   | `/reading/finish`               | Mark a book as finished              |
| GET    | `/reading/current/<user_id>`    | Books a user is currently reading    |
| GET    | `/reading/history/<user_id>`    | Books a user has finished            |
| GET    | `/stats/<user_id>`              | Reading streak, books this month, total pages (supports `?tz=`) |
| GET    | `/stats/<user_id>/genre-streak/<genre>` | Genre-specific reading streak (supports `?tz=`) |

## Lab Completion Summary

This lab was completed using the Elite Engineering SDLC, focusing on:
1. **Diagnosis**: Identified mismatches between docstring contracts and code implementation for streak and history bugs.
2. **Timezone Accuracy**: Extended the streak and monthly stats logic to handle UTC-to-Local conversion via a `tz` query parameter.
3. **Advanced Features**: Implemented Genre-specific streaks.
4. **Accountability**: Recorded design decisions in `docs/adr/0001-streak-logic-extensions.md`.
5. **Verification**: Full coverage via `pytest` unit tests and Playwright headless API tests.

### Mockup of New Stats
```json
{
  "user_id": "4dbd2552...",
  "reading_streak": 3,
  "books_this_month": 3,
  "total_pages_read": 814,
  "genre_streaks": {
    "sci-fi": 2,
    "literary fiction": 1
  }
}
```

## Codebase structure

```plaintext
app.py                  Flask application factory
models.py               SQLAlchemy models: User, Book, ReadingEvent
routes/
  books.py              Book list endpoints
  reading.py            Reading progress endpoints
  stats.py              Statistics endpoint
services/
  reading_service.py    Reading list business logic
  stats_service.py      Statistics calculations
seed_data.py            Database seed script
```

## Running example requests

After seeding, use `curl` or any HTTP client. The seed script prints all three user IDs — use them in the examples below:

```bash
# Get all books
curl http://127.0.0.1:5000/books/

# Get alex's stats (replace USER_ID with the ID printed by seed_data.py)
curl http://127.0.0.1:5000/stats/USER_ID

# Get alex's reading history
curl http://127.0.0.1:5000/reading/history/USER_ID
```
