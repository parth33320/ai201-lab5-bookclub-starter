# Context: BookClub Tinker 5

## Project Goals
The goal of this project is to fix existing bugs in the BookClub application's statistics and reading history features, and then extend the application with advanced features like timezone-aware streaks and genre-specific streaks. We follow the Elite Engineering SDLC, prioritizing alignment, architecture, and live TDD.

## Terminology

### Reading Streak
A **Reading Streak** is the number of consecutive calendar days on which a user has finished at least one book.
- **Grace Period**: A streak is considered "alive" if the user finished a book today OR yesterday.
- **Example**: If today is Monday and the user finished books on Saturday and Sunday, the streak is 2. If the user does not finish a book by the end of Monday, the streak remains 2. If Tuesday passes without a finish, the streak resets to 0.

### Genre Streak
A **Genre Streak** follows the same logic as the Reading Streak but is restricted to books of a specific genre (e.g., "sci-fi"). A user can have multiple concurrent genre streaks.

### Docstring Contract
In this project, docstrings are treated as formal contracts. A function is considered buggy if its implementation deviates from the behavior promised in its docstring. Diagnosis involves identifying the mismatch between the promised behavior (Contract) and the actual behavior (Code).

## Success Criteria
1. **Accuracy**: All statistics (streaks, counts, totals) must be mathematically correct and reflect the actual reading history.
2. **Order**: Reading history must be returned in the order specified by the API contract (most recently finished first).
3. **Robustness**: Timezone differences between the server and the user should not break the perceived streak.
4. **Verifiability**: All changes are verified via live API calls using Playwright and unit tests using pytest.
