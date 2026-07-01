# ADR 0002: Genre-Specific Streaks

## Context
Users want to track their consistency within specific genres (e.g., sci-fi, fantasy).

## Decision
We implemented a `calculate_genre_streak` function in the `stats_service` and added a new API endpoint: `GET /stats/<user_id>/genre-streak/<genre>`.
- The logic mirrors the main `calculate_streak` (including the today/yesterday grace period and timezone awareness) but filters the user's reading history by the specified genre before processing.
- The endpoint returns a JSON object with `user_id`, `genre`, and `streak`.

## Consequences
- Provides deeper analytical value to users.
- Minimal overhead as it reuses the existing `get_reading_history` data.
- Multiple genre streaks can be active at the same time.
