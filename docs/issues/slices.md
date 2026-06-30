# Issue Slices

## Slice 1: Fix calculate_streak() logic (Milestone 3)
- **Diagnosis**: Docstring says streak is based on when a user *finished* a book, but code uses `started_at`.
- **Action**: Change `started_at` to `finished_at` in `services/stats_service.py`.
- **Verification**: `alex` streak should be > 0.

## Slice 2: Fix get_reading_history() sorting (Milestone 4)
- **Diagnosis**: Docstring says history is "most recently finished first", but code orders by `started_at.desc()`.
- **Action**: Change `started_at` to `finished_at` in `ReadingEvent.query.order_by()` in `services/reading_service.py`.
- **Verification**: `alex` history should show the book finished 3 hours ago as the first item.

## Slice 3 (Challenge): Timezone Consistency
- **Goal**: Handle streaks correctly across different timezones.
- **Action**:
  - Update `calculate_streak` to accept an optional `tz_name`.
  - Convert `finished_at` (UTC) to user's local time before extracting `.date()`.
  - Use `datetime.now(tz).date()` instead of `date.today()`.
- **Verification**: Streak remains correct when a timezone is provided.

## Slice 4 (Challenge): Genre Streak Service and Route
- **Goal**: Implement genre-specific streak logic.
- **Action**:
  - Add `calculate_genre_streak(user_id, genre, tz_name)` to `stats_service.py`.
  - Add `GET /stats/<user_id>/genre-streak/<genre>` to `routes/stats.py`.
- **Verification**: `alex` sci-fi streak is correctly calculated.

## Slice 5 (Challenge): Pytest Unit Tests
- **Goal**: Regression testing for core bugs.
- **Action**:
  - Create `tests/test_stats.py` and `tests/test_reading.py`.
  - Mock/Use in-memory DB to verify streak and history sorting logic.
- **Verification**: `pytest` passes.

## Slice 6 (Challenge): Audit and Fix Edge Cases
- **Goal**: Ensure robustness in `books_this_month` and `total_pages_read`.
- **Action**:
  - Audit `books_this_month` for timezone issues (similar to streak).
  - Verify `total_pages_read` handles 0-page books.
- **Verification**: Correct counts even for edge cases.
