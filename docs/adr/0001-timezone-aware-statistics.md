# ADR 0001: Timezone-Aware Statistics

## Context
Reading streaks and monthly finish counts depend on calendar dates. Since the server stores timestamps in UTC, users in different timezones might see their streaks "broken" or their monthly counts off if calculated purely in UTC.

## Decision
We added an optional `tz` query parameter to the statistics endpoints.
- The `calculate_streak` and `books_this_month` functions now accept a `tz_name`.
- We use `pytz` to convert UTC stored timestamps to the user's local timezone before extracting the date.
- If an invalid or missing timezone is provided, we default to UTC to ensure the API remains robust.

## Consequences
- The API response is now more accurate for global users.
- `pytz` is added as a dependency.
- Streak and monthly logic is slightly more complex due to the conversion step.
