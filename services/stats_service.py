"""
services/stats_service.py — BookClub

Computes reading statistics for a user: streak, books finished this month,
and total pages read.
"""

from datetime import date, datetime, timezone
import pytz
from services import reading_service


def calculate_streak(user_id: str, tz_name: str = "UTC") -> int:
    """
    Calculate a user's current reading streak in consecutive days.

    A streak is the number of consecutive calendar days on which the user
    finished at least one book, counting back from today (or yesterday, if
    nothing has been finished today yet).

    Returns 0 if the user has no reading history or if there is a gap of
    more than one day since their most recent finished book.

    Args:
        user_id: ID of the user.
        tz_name: User's local timezone.

    Returns:
        The streak count as an integer.
    """
    # DIAGNOSIS: Docstring says "finished at least one book", Code does "e.started_at.date()"
    events = reading_service.get_reading_history(user_id)
    if not events:
        return 0

    try:
        tz = pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        tz = pytz.UTC

    local_dates = set()
    for e in events:
        local_finish = e.finished_at.replace(tzinfo=pytz.UTC).astimezone(tz)
        local_dates.add(local_finish.date())

    dates = sorted(local_dates, reverse=True)
    today = datetime.now(tz).date()

    if (today - dates[0]).days > 1:
        return 0

    streak = 1
    for i in range(len(dates) - 1):
        delta = (dates[i] - dates[i + 1]).days
        if delta == 1:
            streak += 1
        else:
            break

    return streak


def books_this_month(user_id: str, tz_name: str = "UTC") -> int:
    """
    Count the number of books the user finished in the current calendar month.

    Args:
        user_id: ID of the user.
        tz_name: User's local timezone.

    Returns:
        Count of books finished this month.
    """
    events = reading_service.get_reading_history(user_id)

    try:
        tz = pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        tz = pytz.UTC

    today = datetime.now(tz).date()

    count = 0
    for e in events:
        local_finish = e.finished_at.replace(tzinfo=pytz.UTC).astimezone(tz)
        if local_finish.year == today.year and local_finish.month == today.month:
            count += 1
    return count


def total_pages_read(user_id: str) -> int:
    """
    Sum the page counts of all books the user has finished.

    Args:
        user_id: ID of the user.

    Returns:
        Total pages read as an integer.
    """
    events = reading_service.get_reading_history(user_id)
    # AUDIT: sum() correctly handles 0 pages if a book's pages field is 0.
    return sum(e.book.pages for e in events)


def calculate_genre_streak(user_id: str, genre: str, tz_name: str = "UTC") -> int:
    """
    Calculate a user's current reading streak for a specific genre.

    Args:
        user_id: ID of the user.
        genre:   The genre to filter by.
        tz_name: User's local timezone.

    Returns:
        The genre-specific streak count as an integer.
    """
    events = reading_service.get_reading_history(user_id)
    genre_events = [e for e in events if e.book.genre == genre]

    if not genre_events:
        return 0

    try:
        tz = pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        tz = pytz.UTC

    local_dates = set()
    for e in genre_events:
        local_finish = e.finished_at.replace(tzinfo=pytz.UTC).astimezone(tz)
        local_dates.add(local_finish.date())

    dates = sorted(local_dates, reverse=True)
    today = datetime.now(tz).date()

    if (today - dates[0]).days > 1:
        return 0

    streak = 1
    for i in range(len(dates) - 1):
        delta = (dates[i] - dates[i + 1]).days
        if delta == 1:
            streak += 1
        else:
            break

    return streak
