Tinker 5: BookClub
You've just joined the team maintaining BookClub, a small reading-tracker app. A user filed this bug report:

"My reading streak shows 0 even though I've been finishing books every day this week. The books show up in my history fine — just the streak is wrong."

Your job is to find and fix the bug — and then keep going, because fixing the first bug will reveal a second one that's been hiding in the same codebase.

The point of this lab isn't the fixes. Both fixes are one-word changes. The point is the process: how do you navigate an unfamiliar codebase to find where a bug lives without reading every file, without changing anything speculatively, and without asking someone to just tell you? And how do you verify a fix thoroughly enough that you notice when something else is still wrong?

The skills you'll practice here — reading before touching, reproducing before fixing, tracing a call stack to its root cause, verifying fixes properly — are the same ones that determine how effective you are on your first week at any engineering job.

⚠️ AI tool note: This lab has deliberate slow-down moments where using your AI tool to find the bug would skip exactly the skill being practiced. At those moments, the instructions will say so. There are also orientation moments — understanding what a SQLAlchemy relationship does, or what UniqueConstraint prevents — where asking your AI tool is completely appropriate. The distinction matters: using AI to understand what you're looking at is different from using AI to find what you're looking for.
🎯 Goals
By completing this activity, you will be able to:

Navigate a multi-file Flask application to understand a feature's full data flow before making any changes.
Reproduce a bug from a user report and narrow it to a specific function using live API responses.
Trace a bug through a call stack (route → service → service) by following the data, not guessing.
Identify the mismatch between a docstring's contract and the code's actual behavior as a reliable bug-finding signal.
Distinguish between logic bugs (wrong computed value) and display bugs (correct data, wrong order), and explain why they require different diagnosis paths.

🪄 How this works: Work together as a group throughout the activity using the Driver/Navigator model. The Driver shares their screen and implements the solution while Navigators help guide decisions, ask questions, discuss tradeoffs, and troubleshoot challenges. At each checkpoint, pause to reflect on your group's progress, discuss key implementation decisions, and make sure everyone understands the solution before moving on.
🛠️ Tools and Setup

Fork the BookClub starter repo and clone your fork locally.


Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows

Install dependencies:

pip install -r requirements.txt

Seed the database and start the server:

python seed_data.py    # creates the database and populates test data
python app.py          # starts at http://127.0.0.1:5000
The seed script prints all three user IDs — save them. You'll need them throughout the lab.


Confirm the server is running:

curl http://127.0.0.1:5000/books/
You should get a JSON list of 10 books. If you see an error instead, check that your virtual environment is active and that seed_data.py ran without errors.



Milestone 1: Read the Codebase
⏰ ~15 min

Before you touch anything, read. The bug report tells you which feature is broken — reading streak — but not where in the code that feature lives. Your first job is to build a mental map of the codebase so you know what to look at.

🧠 Before You Start
📔 Layered Architecture - Routes, Services, and Models

This codebase is organized into three layers. Understanding what belongs in each layer is the first thing you need in order to trace a bug — because the layer tells you where to look.

Layer	Files	Responsible for
Routes	routes/stats.py, routes/reading.py	Receiving HTTP requests, calling services, formatting responses. Routes don't compute values — they orchestrate.
Services	services/stats_service.py, services/reading_service.py	Application logic: calculations, rules, data transformation. Services don't know about HTTP.
Models	models.py	Database schema and data structure. Models don't contain business logic.
Why this matters for bug tracing: when an API response returns a wrong value, that's almost certainly a service problem — not a route problem, and not a model problem. Routes call services and format their output; they don't compute values. Models define structure; they don't run calculations.

Good starting point: open the route to understand the call structure (which service functions are called and what they return), then move to the service to trace the logic.

Common mistake: jumping straight to the model file to look for the bug in the data definition. Models almost never contain the logic that produces a wrong computed value. Reading the model is useful for orientation — it's not where you debug.

The call chain you're building in this milestone (route → service → service → model) is what makes that distinction clear before you start debugging.

📔 Docstrings as Contracts

In this codebase, every significant function has a docstring. A docstring isn't just documentation — it's a contract: a written commitment about what the function is supposed to do, what it accepts as input, and what it promises as output.

When a function has a bug, the docstring is often still correct — it describes the intended behavior, and the code drifted from it at some point. That makes the docstring a diagnostic tool.

Instead of asking "what does this code do?" ask: "does this code do what the docstring says it should?" When you find a mismatch, you've found a likely bug location.

Strong signal (mismatch = likely bug):

Docstring: "Returns events ordered by finished_at descending — most recently finished first." Code: order_by(ReadingEvent.started_at.desc())

The docstring names a specific field. The code uses a different field. That mismatch is not ambiguous.

Weak signal (no mismatch, no diagnostic value):

Docstring: "Returns reading events for the user." Code: ReadingEvent.query.filter_by(user_id=user_id).all()

The docstring is too vague to be a contract — it doesn't specify enough to disagree with the code.

The technique works best when you read the docstring before reading the implementation — build the expectation first, then check whether the code honors it. If you read the code first, you'll unconsciously read the docstring through what the code does, and miss the mismatch.


Open README.md and read the codebase structure section. Identify the two directories that contain the application logic and understand what belongs in each. Note which service file would be responsible for the streak calculation.


Read the data model in models.py. Read all three model classes — User, Book, and ReadingEvent. Answer these questions before moving on:

What fields does ReadingEvent have? Which ones are always set, and which can be null?
What does the UniqueConstraint on ReadingEvent prevent?
User has a reading_streak column. Does the stats endpoint use it? (Check routes/stats.py before guessing.)
💡 Orientation moment: If UniqueConstraint is unfamiliar, ask your AI tool to explain what it does with a concrete example — "In SQLAlchemy, what does UniqueConstraint('user_id', 'book_id') on a table prevent?" Understanding the constraint will tell you something important about what the data model allows and what it rules out.

Trace the stats endpoint in routes/stats.py. The endpoint calls three service functions. Identify all three and note what each one is supposed to return according to the route's docstring.


Read the service layer in services/stats_service.py and read all three functions carefully — not just calculate_streak, but all three. For each function, ask: what data does it need, where does it get that data from, and how does it compute its result?

💡 Orientation moment: If the SQLAlchemy relationship loading in these functions is unfamiliar — for example, e.book.pages accessing related data through a relationship — ask your AI tool to explain how SQLAlchemy lazy loading works. Understanding the mechanism will help you reason about edge cases later.
Read the dependency in services/reading_service.py. Read get_reading_history() carefully. Note exactly what the query filters on, what it orders by, and what the function's docstring promises about the result.
💡 Worth noting: get_reading_history() uses .filter(ReadingEvent.finished_at.isnot(None)). That filter makes a specific promise about what the returned events represent. Keep that promise in mind as you read the code that consumes its output.
Before moving to Milestone 2, write out the path from the HTTP request to the streak number. You'll use this map in Milestones 3 and 4, so you should build it now while everything is fresh.
🎯 Real World: The first thing a senior engineer does in an unfamiliar codebase isn't search for the bug — it's build the mental map. Reading before touching, tracing call chains, understanding what each layer promises: these habits determine how effective you are every time you join a new team or inherit code someone else wrote. The engineers who can navigate unfamiliar codebases quickly are the ones who get trusted with the hardest problems.
🤔 Test Yourself
get_reading_history() returns a list of ReadingEvent objects filtered to only include records where finished_at is not None. Why does the function filter this way rather than returning all reading events for the user?
Because events with finished_at = None represent books the user abandoned — they're excluded to keep the history clean and accurate
Because events with finished_at = None are books currently in progress — they haven't been finished, so they don't belong in reading history
Because without the filter, the order_by(finished_at.desc()) clause would place in-progress books at the top of the list, making the history appear in the wrong order
Because finished_at is required by calculate_streak() and total_pages_read() — without the filter, those functions would encounter None dates and raise exceptions

📍 Checkpoint
Before moving on, confirm you can answer these without looking: What are the two ReadingEvent date fields and which is nullable? What does get_reading_history() guarantee about the events it returns? If you're unsure, re-read those two files before moving on — the next three milestones depend on having this clear.



Milestone 2: See Both Bugs in Action
⏰ ~10 min

Before you look at why anything is wrong, confirm you can see it. A bug you haven't reproduced is a bug you haven't understood.


Using the alex user ID printed by seed_data.py:

curl http://127.0.0.1:5000/stats/USER_ID
Record all three values: reading_streak, books_this_month, and total_pages_read.


Hit the history endpoint:

curl http://127.0.0.1:5000/reading/history/USER_ID
Look at the response. Note the order the books come back in — specifically, which book is listed first and what its finished_at date is.


Now let's check the endpoint's promise. Open routes/reading.py and read the docstring for the reading_history function. It makes a specific claim about the order the results should be in. Does the order you got from Step 2 match that claim?


Let's narrow Bug 1. Return to the stats response from Step 1. Two of the three stat values should look correct given what you know about alex's reading history. One should look wrong. Answer these before moving on:

Which stat is wrong? Which are correct?
All three stats functions call get_reading_history(). If get_reading_history() had a bug, all three stats would be wrong. What does it tell you about Bug 1's location that two of the three are correct?
⚠️ Deliberate slow-down: Don't ask your AI tool which stat is wrong or what the bug is. The point of this step is reading the output yourself and reasoning about what it implies — that's the diagnostic skill. The API response is right in front of you; trust your own read.
Look at the finished_at dates in alex's history. Based on those dates alone — not the code — calculate what you'd expect the streak to be. Write it down. You'll use it to verify your fix in Milestone 3.
💡 Two bugs, two paths. You've now seen two things that look wrong: the streak (a computed stat) and the history order (a display issue). These are independent bugs — fixing one won't affect the other. You'll address them in separate milestones so you can trace each one cleanly.
🤔 Test Yourself
Alex's total_pages_read returns the correct value and books_this_month returns the correct value, but reading_streak returns 0. What does this tell you about get_reading_history()?
get_reading_history() has a bug — it's returning the wrong events for the streak calculation, but books_this_month and total_pages_read happen to produce correct values despite using the same broken data
get_reading_history() is returning events in the wrong order, which causes calculate_streak() to mis-count consecutive days but doesn't affect the other two calculations
It's inconclusive — all three stat functions call get_reading_history(), so the bug could still be there or inside any of the three stat functions
get_reading_history() is working correctly — the bug must be inside calculate_streak() specifically, since that's the only function whose output is wrong

📍 Checkpoint
Confirm three things before moving on: (1) you've seen reading_streak: 0 in the API response, (2) you've noted the order the history comes back in and checked it against the route's docstring, and (3) you've written down the streak value you expect a correct implementation to return.



Milestone 3: Trace and Fix Bug 1 - The Streak
⏰ ~10 min

You've narrowed Bug 1 to calculate_streak(). Trace through the function to find the mismatch between what it claims to do and what it actually does.

🧠 Before You Start
📔 Diagnosing Before Fixing

There's a strong temptation, once you spot something suspicious in the code, to change it immediately and see if the tests pass. This works sometimes — and fails in ways that are hard to detect. You change something, the symptom improves, but you've fixed the wrong thing. The real bug is still there, and now it's masked.

The discipline of writing out the diagnosis before touching the code forces you to answer a harder question: why is this the bug, not just a suspicious-looking line?

What diagnosing looks like:

The docstring says: calculates streak from days on which the user finished a book
The code does:      builds a date set using e.started_at — the day books were started
The bug is on line: [the line with started_at]
The fix is:         change started_at to finished_at
What guessing looks like:

"started_at seems off in a streak calculation... let me try changing it to finished_at and see what happens."

Both produce the same fix. The difference is what you've confirmed before applying it. The diagnosis version tells you why started_at is wrong and why finished_at is right — it checks the fix against the docstring before running anything. The guess version tells you the symptom went away, which is not the same as knowing you fixed the root cause.

This also matters when the symptom doesn't change: if you apply a guess and the streak is still 0, you don't know whether your change was wrong or whether there's a second bug masking your fix. If you apply a diagnosed fix and the result is still wrong, you know you need to keep looking — there's more here than you found.

Read the docstring as a contract. Re-open services/stats_service.py. Read the calculate_streak() docstring again, this time as a formal contract:
"A streak is the number of consecutive calendar days on which the user finished at least one book..."

The docstring is precise about which dates the streak counts. Hold that precision in mind while reading the code.

Read through calculate_streak() with this question: does each line do what the docstring says it should? Specifically:
The function builds a set of dates from the reading events. Which field on each event does it use to get those dates?
Is that the same field the docstring is describing?
⚠️ Deliberate slow-down: Don't paste the function into your AI tool and ask it to find the bug. The whole point of this step is reading a contract (the docstring) against an implementation (the code) and spotting the mismatch yourself. That's a pattern you'll use constantly — and the only way to get fast at it is to do it.
You should now see a mismatch between the docstring and the code on a specific line. Write it down in plain language before touching the code:
The docstring says: _______________
The code does:      _______________
The bug is on line: ___
The fix is:         _______________
Writing the diagnosis before applying the fix is what confirms you've actually found the root cause rather than something that merely looked suspicious.

⚠️ Watch Out: The wrong field is a real field on ReadingEvent. It compiles. It returns dates. It's completely plausible-looking. The bug isn't a typo or a missing import — it's using the right data type but the wrong field. This is why reading the docstring as a contract is more reliable than scanning for something that "looks wrong."

Make the one-word change, then save the file.


Reseed the database and restart the server:

python seed_data.py
python app.py
Hit the stats endpoint again and confirm reading_streak now matches the value you predicted in Milestone 2, Step 5. Also confirm that books_this_month and total_pages_read are still correct — a good fix shouldn't break anything that was already working.

Check if Bug 2 is still present. Hit the history endpoint again:
curl http://127.0.0.1:5000/reading/history/USER_ID
Does the history still come back in the wrong order? If so, that confirms the two bugs are independent and you haven't accidentally fixed Bug 2 by fixing Bug 1. Note which book is now listed first.

🤔 Test Yourself
After applying the fix, calculate_streak() collects dates using e.finished_at.date(). Why is the finish date the correct choice here, given that started_at is always set on every ReadingEvent, returns a valid date, and would also compile without error?
Because get_reading_history() already filters to only finished books, so both started_at and finished_at are valid dates for completed reads — either field would identify the same days
Because started_at is a nullable field and could be None on some records, causing the date extraction to raise a TypeError at runtime
Because started_at defaults to the current timestamp when the record is created, making it identical to finished_at in most cases and therefore a reliable proxy for completion date
Because a reading streak measures days on which you completed something — when you start a book is irrelevant to whether you finished one that day

📍 Checkpoint
Confirm all four things before moving on: (1) streak is now the expected value for alex, (2) books_this_month and total_pages_read are still correct, (3) the history endpoint still shows books in the wrong order, and (4) you can explain the Bug 1 fix in one sentence without referring to the code.



Milestone 4: Trace and Fix Bug 2 - The History Order
⏰ ~10 min

The history endpoint returns books in the wrong order — it should be "most recently finished first," but it isn't. Trace this bug the same way you traced the first one: follow the call stack, read the contract, find the mismatch.

🧠 Before You Start
📔 Logic Bugs vs Display Bugs

Bug 1 and Bug 2 look similar on the surface — both were caused by using started_at where finished_at was needed. But they're different categories of mistake, and that difference changes how you diagnose them.

Logic bug (Bug 1 — streak returns 0): The computed value itself is wrong. The function runs to completion and returns a number — it just returns the wrong number. The data going into the function is correct; the calculation is broken.

How to diagnose: trace the calculation — which fields are being read, what the math does with them, what result it produces.

Display bug (Bug 2 — history in wrong order): The data values are correct. All the right books are there, with the right dates. The problem is purely presentation — the records are sorted by the wrong field, so they come back in the wrong sequence.

How to diagnose: don't trace the calculation — look at the sort. The question is only "what is the query ordering by?" not "is the computation right?"

Why the distinction matters: if you misidentify Bug 2 as a logic bug, you'll spend time tracing the history values themselves — checking whether the dates are correct, whether the right books are included — and find nothing wrong. The values ARE correct. The sort is the only thing broken. Recognizing it as a display bug immediately focuses your attention on the one place it could be: the order_by clause.

The diagnostic question:

Is the value wrong? → logic bug → trace the calculation
Are the values right but presented wrong? → display bug → trace the ordering, formatting, or grouping

Let's trace the call stack for the history endpoint. Open routes/reading.py. Find the reading_history() function and read its docstring. Identify the service function it calls.


Open services/reading_service.py. Find get_reading_history() and read it carefully. The query has three clauses — filter_by, filter, and order_by. Focus on order_by:

What field is the query currently ordering by?
What field does the function's docstring say it should order by?

Write the diagnosis before applying the fix:

The docstring says: _______________
The code does:      _______________
The bug is on line: ___
The fix is:         _______________

Make the one-word change, then save the file.


Reseed and restart:

python seed_data.py
python app.py
Hit the history endpoint for alex:

curl http://127.0.0.1:5000/reading/history/USER_ID
The first book in the response should now be the one alex finished most recently (a few hours ago). Confirm by checking its finished_at timestamp. Also confirm the streak is still correct — fixing Bug 2 should not have affected the stats.

Hit the stats endpoint for both other users:
curl http://127.0.0.1:5000/stats/PRIYA_ID
curl http://127.0.0.1:5000/stats/MARCUS_ID
Verify the streak makes sense for each: priya finished her last book over a week ago (streak should be 0), and marcus has no finished books (streak should be 0). Also hit priya's history endpoint and confirm her two books come back most-recently-finished first.

Discussion Prompts
Take a few minutes to talk through these with your group.

You found Bug 2 not from a separate bug report, but while verifying your fix for Bug 1. How does thorough verification change what you find? What would have happened if you had stopped after confirming that reading_streak was now 3?

Both bugs used started_at where finished_at was needed. Should you do a codebase-wide search for other started_at uses after finding this pattern? What's the argument for doing that, and what's the risk?

You were handed a bug report and found both bugs by reading code rather than by adding print statements or using a debugger. In what situations is "read carefully first" faster than "run it with logging"? When is it slower? How do you decide which approach to use?

🤔 Test Yourself
Both bugs involved the same wrong field — started_at used where finished_at was needed. Does that mean they have the same root cause?
Yes — a single find-and-replace of started_at with finished_at across the service layer would have fixed both at once, which means they share a root cause
Yes — both bugs suggest the original developer consistently confused the two fields, which is a single underlying cause that produced two separate symptoms
No — the bugs are in different files and different functions, so they have different root causes by definition
No — the streak bug produced a wrong computed value (a logic error); the history bug produced correct data in the wrong order (a display error). Same wrong field, but different categories of mistake requiring different diagnosis paths
You open an unfamiliar service function. The docstring says it returns "all events where the user completed a chapter." The first line of the function body queries ReadingEvent.query.filter_by(user_id=user_id).all() with no additional filters. What's the most reliable conclusion?
The function is probably fine — docstrings describe intended behavior, and the implementation may handle chapter completion through business logic elsewhere in the pipeline
The docstring and the code are inconsistent — this is a likely bug location, worth tracing before assuming either is correct
The code is correct and the docstring is outdated — when the two disagree, the code is always more authoritative than documentation
This is a documentation debt issue, not a bug — the missing filter doesn't affect behavior because all events are associated with the user anyway
After fixing both bugs, a teammate proposes a different fix for Bug 1: instead of changing started_at to finished_at in calculate_streak(), they suggest modifying get_reading_history() to set started_at equal to finished_at before returning the events. This would also make the streak return the correct value. What's wrong with this approach?
Nothing — both fixes produce the same result for the streak, so either approach is equally valid
It would cause books_this_month and total_pages_read to break, since they also call get_reading_history() and would receive incorrect started_at values
It mutates data returned from a query, which would overwrite the actual started_at values and corrupt them for any other caller of get_reading_history() — or any future code that needs the real start date
It won't work because SQLAlchemy model instances returned from a query are read-only — assigning to e.started_at raises an AttributeError
A user reports: "The app shows I've read 0 pages total, but my reading history lists three books correctly." You open stats_service.py and find total_pages_read(), which calls get_reading_history() and returns sum(e.book.pages for e in events). No exception is thrown — the function silently returns 0. Which of the following is the most likely explanation?
get_reading_history() is returning an empty list — but this would contradict the user's report that their history correctly shows three books
The Book model stores pages as a string rather than an integer — but sum() on strings raises TypeError, not a silent 0
The book relationship on ReadingEvent is broken, so e.book is None for every event — but accessing None.pages raises AttributeError, not a silent 0
The three books in the database have pages = 0, so sum(0 + 0 + 0) returns 0 correctly — the data is wrong, not the code

📍 Checkpoint
Verify all five things: (1) streak is the correct value for alex, (2) history for alex shows the most recently finished book first, (3) priya's streak is 0 and her history is in the right order, (4) marcus's streak is 0, and (5) you can explain both fixes in one sentence each without referring to the code.



Optional Challenges
If your group finishes early, pair up and take one of these on together:


Extend the streak logic. The current implementation starts the streak from today and walks backward. But what if a user finishes a book at 11:58 PM and the server clock is in a different timezone? Trace where timezone handling happens (or doesn't happen) in calculate_streak() and mark_as_finished(). Write a version of calculate_streak() that handles UTC-stored timestamps consistently with the user's local date.


Add a genre streak. The current streak counts any finished book. Design and implement a calculate_genre_streak(user_id, genre) function that counts consecutive days on which the user finished at least one book in a specific genre. Add a route GET /stats/<user_id>/genre-streak/<genre> that returns it. Test it against the seed data — which genre gives alex the longest streak?


Write a test. Both bugs you fixed would have been caught by unit tests. Write a test for calculate_streak() that creates a user with reading events spanning three consecutive days and asserts the streak is 3. Then write a test for get_reading_history() that creates a user with two finished books and asserts the results come back most-recently-finished first. Use pytest and a SQLite in-memory database.


Audit the other stats. You confirmed books_this_month() and total_pages_read() are working correctly — but are they correct by design, or correct by coincidence? Read both functions carefully and write down one edge case for each that could produce a wrong result. For books_this_month(), what happens on the first day of a month if the user finished a book the previous night in a different timezone? For total_pages_read(), what happens if a book's pages field is 0?
