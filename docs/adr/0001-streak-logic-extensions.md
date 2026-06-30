# ADR 0001: Streak Logic Extensions (Timezone & Genre)

## Status
Accepted

## Context
The BookClub application calculates reading streaks based on the dates books were finished. The original implementation had two major limitations:
1. It used server local time (`date.today()`) and UTC timestamps for `finished_at` interchangeably, which could lead to incorrect streaks for users in different timezones.
2. It only calculated a global streak, not accounting for specific reading interests (genres).

## Decision
1. **Timezone Handling**:
   - The `calculate_streak` service and related stats functions will accept an optional `tz_name` (e.g., `America/New_York`).
   - All UTC timestamps (`finished_at`) will be converted to the user's local timezone before extracting the date.
   - If no timezone is provided, it defaults to `UTC`.
   - The API will expose this via a `?tz=` query parameter.

2. **Genre Streaks**:
   - A new service function `calculate_genre_streak` will be implemented.
   - It will filter the reading history by the specified genre before applying the streak calculation logic.
   - A new endpoint `GET /stats/<user_id>/genre-streak/<genre>` will be added.

## Consequences
- **Positive**: Accurate streaks for global users; more granular engagement metrics via genre streaks.
- **Neutral**: Slightly more complex service layer logic; requirement for clients to pass timezone information for maximum accuracy.
- **Negative**: Increased dependency on a timezone library (e.g., `pytz` or Python 3.9+ `zoneinfo`).
