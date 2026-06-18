# Job Search Automation Lab Notes

## Project Identity

This project started as a Python learning exercise using JobSpy, but it is now evolving into a broader job search automation system.

The project name is:

Job Search Automation Lab

The current first module focuses on collecting job postings using JobSpy.

## Project Goal

Build a Python project that collects job postings using JobSpy, inspects the returned data, and saves the results for later processing.

## Current Milestone 1

We created the first working script in src/main.py.

The script does the following:

1. Imports scrape_jobs from JobSpy.
2. Searches Indeed for Python Developer jobs in Dallas, TX.
3. Requests 10 results.
4. Receives the result as a Pandas DataFrame.
5. Prints total job count.
6. Prints all returned columns.
7. Prints the first few rows.
8. Saves the results to data/processed/jobs.csv.

## Important Columns Returned

Useful columns returned by JobSpy:

- id
- site
- job_url
- title
- company
- location
- date_posted
- job_type
- is_remote
- description
- skills
- experience_range

## First Observation

JobSpy successfully returned job postings from Indeed.

The date_posted column exists, which means we can later build filters like jobs posted today, jobs posted in the last 24 hours, or jobs posted in the last 7 days.

However, the current date_posted values are date-based, not exact timestamp-based.

## Milestone 2: Raw and Clean Job Output Pipeline

In Milestone 2, we improved the original single-output script into a small data pipeline.

The pipeline flow is:

Collect jobs
→ Save raw jobs
→ Select useful columns
→ Save cleaned jobs
→ Print summary

### Raw Data

Raw data means the original data collected from the source before changing or reducing it.

In this project, raw data is saved to:

data/raw/jobs_raw.csv

This file contains the full JobSpy output with all available columns.

Keeping raw data is important because it allows us to reprocess the original data later if our cleaning logic changes.

### Processed Data

Processed data means data that has been cleaned, reduced, or transformed for easier use.

In this project, processed data is saved to:

data/processed/jobs_clean.csv

This file keeps only the columns we currently need:

- site
- title
- company
- location
- date_posted
- job_type
- is_remote
- job_url

### Why We Used Functions

We split the script into functions so each function has one clear responsibility.

Current functions:

- collect_jobs()
- save_raw_jobs()
- clean_jobs()
- save_clean_jobs()
- print_summary()
- main()

This makes the code easier to read, debug, test, and improve.

### Why We Used pathlib.Path

We used pathlib.Path to handle file paths in a clean Python way.

Example:

RAW_OUTPUT_PATH = Path("data/raw/jobs_raw.csv")

This makes file path handling more readable and gives useful methods like:

RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

That line makes sure the output folder exists before saving the CSV file.

### What clean_jobs() Does

The clean_jobs() function takes the full raw JobSpy DataFrame and selects only the useful columns.

The raw data had 34 columns.

The cleaned data keeps 8 columns.

This is our first transformation step.

### Why Generated CSV Files Are Ignored by Git

The CSV files are generated outputs.

They can be recreated by running the script again.

So we do not commit them to Git.

We commit the code that creates them, not the generated files themselves.

## Milestone 3: Search Configuration File

In Milestone 3, we moved the search settings out of Python code and into a JSON configuration file.

Before this milestone, the search values were hardcoded inside `src/main.py`.

Example:

```python
search_term="Python Developer"
location="Dallas, TX"
results_wanted=10
```

## Milestone 4: Multi-Search Job Collection

### What we built

We upgraded the job collection pipeline from a single search term to multiple search terms.

Previously, the config file had one value:

```json
"search_term": "Python Developer"
```

Now, the config file uses a list:

```json
"search_terms": [
  "Python Developer",
  "Data Engineer",
  "SQL Developer"
]
```

This allows the same Python program to collect jobs for multiple roles without changing the source code.

### Why this matters

This is an example of config-driven design.

Instead of hardcoding search terms inside Python, we keep them in a JSON config file. This makes the system easier to modify, reuse, and expand.

In a real production project, business rules, search settings, file paths, API settings, and environment-specific values are often kept outside the main code.

### New Python concepts used

#### 1. Looping through a list

```python
for search_term in config["search_terms"]:
```

This loop takes each role from the config list and runs the job collection process one by one.

#### 2. Creating a reusable function for one search

```python
def collect_jobs_for_search_term(config, search_term):
```

This function handles one job search at a time. It makes the code easier to understand and reuse.

#### 3. Adding a new column to a DataFrame

```python
jobs["search_term"] = search_term
```

This adds a new column to every collected job row. The column tells us which search term produced that job.

This is important because after combining multiple searches, we still need to know where each job came from.

#### 4. Combining multiple DataFrames

```python
combined_jobs = pd.concat(all_jobs, ignore_index=True)
```

`pd.concat()` combines multiple DataFrames into one DataFrame.

`ignore_index=True` resets the row numbers so the final combined DataFrame has a clean index.

### New pipeline flow

```text
Load config
    ↓
Read search_terms list
    ↓
Loop through each search term
    ↓
Collect jobs using JobSpy
    ↓
Add search_term column
    ↓
Store each result in a list
    ↓
Combine all job results with pd.concat()
    ↓
Save raw jobs
    ↓
Create cleaned jobs
    ↓
Save cleaned jobs
```

### Result

The script successfully collected 30 jobs:

```text
3 search terms × 10 jobs each = 30 jobs
```

The cleaned output now includes the `search_term` column, which prepares the project for future filtering, deduplication, analytics, and dashboard features.

### Industry terms connected to this milestone

- Config-driven design
- Batch collection
- Iterative processing
- DataFrame concatenation
- Metadata tagging
- Data pipeline expansion

## Milestone 5: Deduplicate Jobs by URL

### What we built

We added a deduplication step to the job collection pipeline.

After collecting jobs from multiple search terms, the same job can appear more than once. For example, one job posting may appear under both `Python Developer` and `Data Engineer`.

To handle this, we added a new function:

```python
def deduplicate_jobs(jobs):
    deduplicated_jobs = jobs.drop_duplicates(subset=["job_url"]).copy()

    return deduplicated_jobs
```

### Why this matters

This is a data quality improvement.

When a pipeline collects data from multiple searches or multiple sources, duplicate records are common. If duplicates are not removed, our final dataset can become misleading.

For example:

```text
Raw jobs collected: 30
Clean jobs saved: 30
```

may look correct, but if 5 of those jobs are duplicates, then we only have 25 unique jobs.

Deduplication helps make the cleaned output more accurate.

### Why we use job_url

We used `job_url` as the deduplication key.

```python
jobs.drop_duplicates(subset=["job_url"])
```

This means:

```text
If two or more rows have the same job_url, treat them as the same job posting.
```

A job URL is usually a strong identifier because each posting normally has a unique link.

### Why raw output is saved before deduplication

We save the raw file before removing duplicates:

```text
Collect jobs
    ↓
Save raw jobs
    ↓
Deduplicate jobs
    ↓
Clean jobs
    ↓
Save clean jobs
```

This is useful because raw data shows exactly what came from the source before our pipeline changed anything.

In production data pipelines, keeping raw data is important for debugging, auditing, and reprocessing.

### Why clean output is saved after deduplication

The clean output is meant to be useful for analysis.

So we remove duplicate jobs before creating the clean file.

This means:

```text
raw/jobs_raw.csv = original collected data
processed/jobs_clean.csv = cleaned and deduplicated data
```

### New Pandas concept used

#### drop_duplicates()

```python
jobs.drop_duplicates(subset=["job_url"])
```

`drop_duplicates()` removes repeated rows.

The `subset` parameter tells Pandas which column to use when checking duplicates.

In our case:

```python
subset=["job_url"]
```

means Pandas only checks the `job_url` column.

### New pipeline flow

```text
Load config
    ↓
Collect jobs for multiple search terms
    ↓
Save raw collected jobs
    ↓
Remove duplicate jobs using job_url
    ↓
Select useful columns
    ↓
Save cleaned jobs
    ↓
Print summary with raw, unique, and clean job counts
```

### Result

In the latest run, the pipeline collected 30 jobs:

```text
Raw jobs collected: 30
Unique jobs after deduplication: 30
Clean jobs saved: 30
```

This means no duplicate job URLs were found in that run.

Even though no rows were removed, the pipeline now has protection against duplicates in future runs.

### Industry terms connected to this milestone

- Deduplication
- Data quality rule
- Unique identifier
- Raw layer
- Processed layer
- Auditability
- Reprocessing
- Data cleaning
