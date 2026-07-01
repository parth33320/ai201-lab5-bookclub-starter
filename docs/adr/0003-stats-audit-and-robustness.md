# ADR 0003: Stats Audit & Robustness

## Context
We audited the statistics calculation logic to identify potential edge cases or bugs.

## Findings

### Total Pages Read
- **Edge Case**: What happens if a book has `pages = 0`?
- **Analysis**: The current implementation `sum(e.book.pages for e in events)` correctly handles `0`. It will simply add `0` to the total, which is mathematically correct (if a book has 0 pages, reading it adds 0 to the total).
- **Decision**: No code change needed, added an audit comment to `total_pages_read`.

### Books This Month
- **Edge Case**: What happens on the first day of the month for users in different timezones?
- **Analysis**: If a user finishes a book on the last day of Month N at 11:00 PM local time, but it's already 3:00 AM UTC on the first day of Month N+1, the book should count towards Month N.
- **Decision**: The timezone-aware implementation in `books_this_month` handles this correctly by converting the UTC `finished_at` to local time before checking the year and month.

### 0-Page Books and Division
- **Analysis**: There are no divisions performed on the page count in the current statistics, so there is no risk of `ZeroDivisionError`.

## Consequences
- Increased confidence in the robustness of the statistics logic.
- Documentation of considered edge cases prevents future "fixes" that might introduce bugs.
